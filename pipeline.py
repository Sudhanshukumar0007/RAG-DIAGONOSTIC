"""
pipeline.py — Steps 5 + 6
===========================
LangGraph RAG pipeline with two nodes:
  1. retrieve — embed query → Chroma top-5 → attach metadata + similarity scores
  2. generate — RAG prompt → Groq LLM → answer

LangSmith tracing is configured via environment variables (LANGCHAIN_TRACING_V2,
LANGCHAIN_API_KEY, LANGCHAIN_PROJECT). Every graph run is automatically traced.

This module exposes:
  build_graph()  — builds and compiles the LangGraph StateGraph
  run_query()    — convenience wrapper: runs one query through the graph

Run standalone to smoke-test with a single query:
    python pipeline.py
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Annotated, Any

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from groq import Groq
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph
from sentence_transformers import SentenceTransformer
from typing_extensions import TypedDict

from shared_logger import get_logger

# ─── Setup ────────────────────────────────────────────────────────────────────
load_dotenv()
log = get_logger()

GROQ_MODEL = "openai/gpt-oss-20b"
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "rag_diagnostic"
TOP_K = 5

RAG_SYSTEM_PROMPT = (
    "You are a factual assistant. Answer the question using ONLY the provided context. "
    "If the context does not contain enough information to answer, say exactly: "
    "'The context does not contain enough information to answer this question.' "
    "Do not make up facts. Be concise."
)

RAG_USER_TEMPLATE = """\
Context:
{context}

Question: {query}

Answer:"""


# ─── Singletons (lazy-loaded, cached after first call) ────────────────────────
_embedding_model: SentenceTransformer | None = None
_chroma_collection: chromadb.Collection | None = None
_groq_client: Groq | None = None


def _get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        log.info("Loading embedding model: %s", EMBEDDING_MODEL_NAME)
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        log.info("Embedding model ready.")
    return _embedding_model


def _get_chroma_collection() -> chromadb.Collection:
    global _chroma_collection
    if _chroma_collection is None:
        if not CHROMA_DIR.exists():
            raise RuntimeError(
                f"Chroma DB not found at {CHROMA_DIR}. "
                "Run build_index.py first."
            )
        client = chromadb.PersistentClient(
            path=str(CHROMA_DIR),
            settings=Settings(anonymized_telemetry=False),
        )
        _chroma_collection = client.get_collection(COLLECTION_NAME)
        log.info("Chroma collection '%s' loaded (%d docs).", COLLECTION_NAME, _chroma_collection.count())
    return _chroma_collection


def _get_groq_client() -> Groq:
    global _groq_client
    if _groq_client is None:
        key = os.getenv("GROQ_API_KEY", "")
        if not key or key == "your_groq_api_key_here":
            raise RuntimeError("GROQ_API_KEY is not set in .env")
        _groq_client = Groq(api_key=key)
        log.info("Groq client initialized.")
    return _groq_client


# ─── LangGraph State ──────────────────────────────────────────────────────────

class RAGState(TypedDict):
    """Typed state for the LangGraph RAG graph."""
    query: str
    language: str
    query_id: str
    retrieved_chunks: list[dict]   # filled by retrieve node
    generated_answer: str          # filled by generate node


# ─── Nodes ────────────────────────────────────────────────────────────────────

def retrieve_node(state: RAGState) -> dict:
    """Embed the query and retrieve top-K chunks from Chroma."""
    query = state["query"]
    query_id = state.get("query_id", "unknown")
    language = state.get("language", "unknown")

    log.debug("[%s] RETRIEVE | lang=%s | query=%r", query_id, language, query[:80])

    model = _get_embedding_model()
    collection = _get_chroma_collection()

    query_embedding = model.encode([query], normalize_embeddings=True)[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for rank, (doc, meta, dist) in enumerate(
        zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ):
        # Chroma with cosine space returns distance (lower = more similar)
        # Convert distance to similarity: similarity = 1 - distance
        similarity = 1.0 - float(dist)
        chunk = {
            "rank": rank + 1,
            "chunk_id": meta.get("chunk_id", f"unknown_{rank}"),
            "topic": meta.get("topic", "unknown"),
            "language": meta.get("language", "unknown"),
            "source_doc": meta.get("source_doc", "unknown"),
            "similarity_score": round(similarity, 6),
            "text": doc,
        }
        chunks.append(chunk)
        log.debug(
            "  Rank %d: chunk_id=%s topic=%s lang=%s sim=%.4f",
            rank + 1, chunk["chunk_id"], chunk["topic"], chunk["language"], similarity,
        )

    log.info(
        "[%s] Retrieved %d chunks | top sim=%.4f | top chunk topic=%s lang=%s",
        query_id, len(chunks),
        chunks[0]["similarity_score"] if chunks else 0.0,
        chunks[0]["topic"] if chunks else "N/A",
        chunks[0]["language"] if chunks else "N/A",
    )

    return {"retrieved_chunks": chunks}


def generate_node(state: RAGState) -> dict:
    """Construct RAG prompt and call Groq to generate an answer."""
    query = state["query"]
    query_id = state.get("query_id", "unknown")
    chunks = state.get("retrieved_chunks", [])

    if not chunks:
        log.warning("[%s] No chunks retrieved — returning empty answer.", query_id)
        return {"generated_answer": "No context was retrieved."}

    # Build context string from retrieved chunks
    context_parts = []
    for chunk in chunks:
        header = f"[Source: {chunk['topic']} ({chunk['language']}), Similarity: {chunk['similarity_score']:.4f}]"
        context_parts.append(f"{header}\n{chunk['text']}")
    context = "\n\n---\n\n".join(context_parts)

    user_message = RAG_USER_TEMPLATE.format(context=context, query=query)

    log.debug("[%s] GENERATE | context_len=%d chars", query_id, len(context))
    log.debug("[%s] Full context:\n%s", query_id, context[:500])

    groq_client = _get_groq_client()
    for attempt in range(1, 4):
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": RAG_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.1,
                max_tokens=1024,  # Qwen3 thinking model uses tokens for <think> block
            )
            answer = response.choices[0].message.content or ""
            # Strip Qwen3 thinking block before returning answer
            answer = re.sub(r"<think>[\s\S]*?</think>", "", answer, flags=re.IGNORECASE).strip()
            log.info("[%s] Answer: %s", query_id, answer[:120])
            return {"generated_answer": answer}

        except Exception as exc:  # noqa: BLE001
            log.warning("[%s] Groq error attempt %d: %s", query_id, attempt, exc)
            err_str = str(exc)
            if "429" in err_str or "rate_limit" in err_str:
                time.sleep(6.0 * attempt)
            else:
                time.sleep(2.0 * attempt)

    log.error("[%s] All Groq attempts failed — returning error string.", query_id)
    return {"generated_answer": "ERROR: LLM call failed after 3 attempts."}


# ─── Graph Construction ────────────────────────────────────────────────────────

def build_graph():
    """Build and compile the LangGraph RAG StateGraph."""
    graph = StateGraph(RAGState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    compiled = graph.compile()
    log.info("LangGraph compiled: START → retrieve → generate → END")
    return compiled


# ─── Convenience wrapper ──────────────────────────────────────────────────────

def run_query(
    compiled_graph,
    query_text: str,
    language: str,
    query_id: str,
) -> dict:
    """
    Run a single query through the compiled LangGraph graph.
    Returns the final state dict.
    """
    initial_state: RAGState = {
        "query": query_text,
        "language": language,
        "query_id": query_id,
        "retrieved_chunks": [],
        "generated_answer": "",
    }

    config = {
        "run_name": f"rag_query_{query_id}",
        "metadata": {
            "query_id": query_id,
            "language": language,
            "query_text": query_text,
        },
    }

    final_state = compiled_graph.invoke(initial_state, config=config)
    return final_state


# ─── Smoke test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Smoke test: running one English query through the pipeline…")
    graph = build_graph()
    result = run_query(
        graph,
        query_text="What is the capital of Rajasthan?",
        language="en",
        query_id="smoke_test_rajasthan_q0_en",
    )
    print("\n── Smoke Test Result ──")
    print(f"Query   : {result['query']}")
    print(f"Answer  : {result['generated_answer']}")
    print(f"Top chunk: {result['retrieved_chunks'][0]['chunk_id']} | "
          f"topic={result['retrieved_chunks'][0]['topic']} | "
          f"sim={result['retrieved_chunks'][0]['similarity_score']:.4f}")
