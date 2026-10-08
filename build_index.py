"""
build_index.py — Steps 2 + 3
==============================
1. Loads all articles from data/raw/*.txt
2. Chunks with RecursiveCharacterTextSplitter (chunk_size=500, overlap=50)
3. Embeds with paraphrase-multilingual-MiniLM-L12-v2
4. Stores in a single shared Chroma collection at ./chroma_db

Idempotent: if the Chroma collection already has documents, skips re-embedding.

Run:
    python build_index.py
"""

import json
import os
import sys
from pathlib import Path

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from shared_logger import get_logger

# ─── Setup ────────────────────────────────────────────────────────────────────
load_dotenv()
log = get_logger()

RAW_DIR = Path("data/raw")
CHROMA_DIR = Path("chroma_db")
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
COLLECTION_NAME = "rag_diagnostic"
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Map raw file names back to topic keys
TOPIC_KEYS = [
    "rajasthan", "kerala", "punjab", "maharashtra",
    "uttar_pradesh", "bihar", "gujarat", "tamil_nadu",
]


def load_raw_articles() -> list[dict]:
    """Load all *.txt files from data/raw and return list of article dicts."""
    articles = []
    for txt_file in sorted(RAW_DIR.glob("*.txt")):
        name = txt_file.stem  # e.g. "rajasthan_en"
        parts = name.rsplit("_", 1)
        if len(parts) != 2 or parts[1] not in ("en", "hi"):
            log.warning("Unexpected filename format: %s — skipping", txt_file.name)
            continue
        topic, lang = parts[0], parts[1]
        text = txt_file.read_text(encoding="utf-8")
        articles.append(
            {"topic": topic, "language": lang, "source_doc": txt_file.name, "text": text}
        )
    log.info("Loaded %d raw article files", len(articles))
    return articles


def chunk_articles(articles: list[dict]) -> list[dict]:
    """Chunk each article and return a flat list of chunk dicts with metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    all_chunks: list[dict] = []
    for art in articles:
        chunks = splitter.split_text(art["text"])
        for idx, chunk_text in enumerate(chunks):
            chunk_id = f"{art['topic']}_{art['language']}_chunk{idx:04d}"
            all_chunks.append(
                {
                    "chunk_id": chunk_id,
                    "topic": art["topic"],
                    "language": art["language"],
                    "source_doc": art["source_doc"],
                    "text": chunk_text,
                }
            )
        log.debug(
            "  %s_%s → %d chunks",
            art["topic"], art["language"], len(chunks),
        )
    log.info("Total chunks created: %d", len(all_chunks))
    return all_chunks


def embed_and_store(chunks: list[dict]) -> None:
    """Embed all chunks and store them in Chroma."""
    log.info("Loading embedding model: %s", EMBEDDING_MODEL_NAME)
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    sample_embedding = model.encode(["test"])
    embedding_dim = len(sample_embedding[0])
    log.info("Embedding model loaded — dimension: %d", embedding_dim)

    # Save model info for later reference
    model_info = {"model_name": EMBEDDING_MODEL_NAME, "embedding_dim": embedding_dim}
    Path("data/embedding_model_info.json").write_text(
        json.dumps(model_info, indent=2), encoding="utf-8"
    )
    log.info("Embedding model info saved to data/embedding_model_info.json")
    print(f"\n{'='*50}")
    print(f"Embedding model : {EMBEDDING_MODEL_NAME}")
    print(f"Embedding dim   : {embedding_dim}")
    print(f"{'='*50}\n")

    # ── Chroma setup ──
    chroma_client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )

    # Check if collection already has data
    existing_collections = [c.name for c in chroma_client.list_collections()]
    if COLLECTION_NAME in existing_collections:
        collection = chroma_client.get_collection(COLLECTION_NAME)
        count = collection.count()
        if count > 0:
            log.info(
                "Chroma collection '%s' already has %d documents — skipping re-embedding.",
                COLLECTION_NAME, count,
            )
            log.info("Delete ./chroma_db to force a fresh rebuild.")
            return
    else:
        collection = chroma_client.create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    log.info("Embedding %d chunks (this may take a minute)…", len(chunks))

    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    metadatas = [
        {
            "topic": c["topic"],
            "language": c["language"],
            "source_doc": c["source_doc"],
            "chunk_id": c["chunk_id"],
        }
        for c in chunks
    ]

    # Embed in batches to avoid memory spikes
    BATCH_SIZE = 64
    all_embeddings = []
    for i in tqdm(range(0, len(texts), BATCH_SIZE), desc="Embedding batches"):
        batch = texts[i : i + BATCH_SIZE]
        embeddings = model.encode(batch, show_progress_bar=False, normalize_embeddings=True)
        all_embeddings.extend(embeddings.tolist())

    log.info("Adding %d chunks to Chroma…", len(chunks))
    # Chroma add in batches (max 5461 per call to avoid gRPC limit)
    CHROMA_BATCH = 500
    for i in tqdm(range(0, len(chunks), CHROMA_BATCH), desc="Storing in Chroma"):
        collection.add(
            ids=ids[i : i + CHROMA_BATCH],
            documents=texts[i : i + CHROMA_BATCH],
            embeddings=all_embeddings[i : i + CHROMA_BATCH],
            metadatas=metadatas[i : i + CHROMA_BATCH],
        )

    final_count = collection.count()
    log.info("✓ Chroma collection '%s' now has %d documents.", COLLECTION_NAME, final_count)


def main() -> None:
    log.info("=" * 60)
    log.info("STEP 2+3 — Chunk Articles & Build Vector Index")
    log.info("=" * 60)

    # Check raw articles exist
    txt_files = list(RAW_DIR.glob("*.txt"))
    if len(txt_files) == 0:
        log.error("No .txt files found in %s — run fetch_articles.py first.", RAW_DIR)
        sys.exit(1)

    articles = load_raw_articles()
    chunks = chunk_articles(articles)
    embed_and_store(chunks)

    log.info("STEP 2+3 complete.\n")


if __name__ == "__main__":
    main()
