"""
run_experiment.py — Step 6
===========================
Runs all 72 queries from data/queries.json through the LangGraph RAG pipeline.

Writes:
  results/results.csv            — one row per query (with 2 blank annotation cols)
  results/retrieved_chunks.jsonl — top-3 chunk texts per query for manual annotation

Run:
    python run_experiment.py
"""

import csv
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from tqdm import tqdm

from pipeline import build_graph, run_query
from shared_logger import get_logger

# ─── Setup ────────────────────────────────────────────────────────────────────
load_dotenv()
log = get_logger()

QUERIES_PATH = Path("data/queries.json")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_CSV = RESULTS_DIR / "results.csv"
CHUNKS_JSONL = RESULTS_DIR / "retrieved_chunks.jsonl"

# LangSmith project URL base — used to construct per-run URLs
LANGSMITH_PROJECT = os.getenv("LANGCHAIN_PROJECT", "hinglish-rag-diagnostic")
LANGCHAIN_TRACING = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"

CSV_FIELDNAMES = [
    "query_id",
    "topic",
    "language",
    "query_text",
    "retrieved_chunk_ids",
    "retrieved_chunk_languages",
    "retrieved_chunk_topics",
    "top_similarity_score",
    "generated_answer",
    "langsmith_trace_url",
    "retrieval_correct",   # blank — human fills in
    "answer_faithful",     # blank — human fills in
]

RATE_LIMIT_SLEEP = 2.5  # seconds between Groq calls (keeps TPM below 8000 limit)


def get_langsmith_project_url() -> str:
    """Return a base URL for the LangSmith project (best-effort)."""
    if LANGCHAIN_TRACING:
        return f"https://smith.langchain.com/project/{LANGSMITH_PROJECT}"
    return "tracing_disabled"


def main() -> None:
    log.info("=" * 60)
    log.info("STEP 6 — Run Experiment (72 queries)")
    log.info("=" * 60)

    # ── Validate prerequisites ──
    groq_key = os.getenv("GROQ_API_KEY", "")
    if not groq_key or groq_key == "your_groq_api_key_here":
        log.error("GROQ_API_KEY is not set in .env — please fill it in and retry.")
        sys.exit(1)

    if not QUERIES_PATH.exists():
        log.error("queries.json not found — run generate_queries.py first.")
        sys.exit(1)

    queries = json.loads(QUERIES_PATH.read_text(encoding="utf-8"))
    log.info("Loaded %d queries from %s", len(queries), QUERIES_PATH)

    if len(queries) != 72:
        log.warning("Expected 72 queries but got %d — check generate_queries.py output.", len(queries))

    if LANGCHAIN_TRACING:
        log.info("LangSmith tracing ENABLED — project: %s", LANGSMITH_PROJECT)
    else:
        log.info("LangSmith tracing DISABLED (set LANGCHAIN_API_KEY to enable)")

    # ── Build the graph once ──
    log.info("Building LangGraph…")
    graph = build_graph()
    log.info("Graph ready.")

    project_url = get_langsmith_project_url()

    # ── Run all queries ──
    results_rows: list[dict] = []
    chunks_records: list[dict] = []

    for i, query_entry in enumerate(tqdm(queries, desc="Running queries")):
        query_id = query_entry["query_id"]
        topic = query_entry["topic"]
        language = query_entry["language"]
        query_text = query_entry["query_text"]

        log.info(
            "\n[%d/%d] query_id=%s | lang=%s | query=%r",
            i + 1, len(queries), query_id, language, query_text[:80],
        )

        try:
            state = run_query(graph, query_text, language, query_id)
        except Exception as exc:  # noqa: BLE001
            log.error("EXCEPTION for query_id=%s: %s", query_id, exc)
            # Write a placeholder row so we don't lose track of this query
            results_rows.append(
                {
                    "query_id": query_id,
                    "topic": topic,
                    "language": language,
                    "query_text": query_text,
                    "retrieved_chunk_ids": "ERROR",
                    "retrieved_chunk_languages": "ERROR",
                    "retrieved_chunk_topics": "ERROR",
                    "top_similarity_score": "",
                    "generated_answer": f"ERROR: {exc}",
                    "langsmith_trace_url": project_url,
                    "retrieval_correct": "",
                    "answer_faithful": "",
                }
            )
            time.sleep(RATE_LIMIT_SLEEP)
            continue

        chunks = state.get("retrieved_chunks", [])
        answer = state.get("generated_answer", "")

        # Flatten lists for CSV
        chunk_ids = [c["chunk_id"] for c in chunks]
        chunk_langs = [c["language"] for c in chunks]
        chunk_topics = [c["topic"] for c in chunks]
        top_sim = chunks[0]["similarity_score"] if chunks else ""

        # LangSmith trace URL — best-effort; actual per-run URL requires SDK inspection
        # With tracing enabled, each run is recorded; we link to project-level view
        trace_url = project_url if LANGCHAIN_TRACING else "tracing_disabled"

        results_rows.append(
            {
                "query_id": query_id,
                "topic": topic,
                "language": language,
                "query_text": query_text,
                "retrieved_chunk_ids": json.dumps(chunk_ids, ensure_ascii=False),
                "retrieved_chunk_languages": json.dumps(chunk_langs),
                "retrieved_chunk_topics": json.dumps(chunk_topics),
                "top_similarity_score": top_sim,
                "generated_answer": answer,
                "langsmith_trace_url": trace_url,
                "retrieval_correct": "",    # human fills in
                "answer_faithful": "",      # human fills in
            }
        )

        # Top-3 chunk texts for retrieved_chunks.jsonl
        top3 = [
            {
                "rank": c["rank"],
                "chunk_id": c["chunk_id"],
                "topic": c["topic"],
                "chunk_language": c["language"],
                "similarity_score": c["similarity_score"],
                "chunk_text": c["text"],
            }
            for c in chunks[:3]
        ]
        chunks_records.append(
            {
                "query_id": query_id,
                "query_text": query_text,
                "language": language,
                "expected_source_topic": query_entry.get("expected_source_topic", topic),
                "generated_answer": answer,
                "top_3_chunks": top3,
            }
        )

        time.sleep(RATE_LIMIT_SLEEP)  # polite rate limiting

    # ── Write results.csv ──
    with RESULTS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(results_rows)
    log.info("\n✓ Saved results.csv: %s (%d rows)", RESULTS_CSV, len(results_rows))

    # ── Write retrieved_chunks.jsonl ──
    with CHUNKS_JSONL.open("w", encoding="utf-8") as f:
        for record in chunks_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    log.info("✓ Saved retrieved_chunks.jsonl: %s (%d records)", CHUNKS_JSONL, len(chunks_records))

    # ── Summary ──
    by_lang: dict[str, int] = {}
    for row in results_rows:
        by_lang[row["language"]] = by_lang.get(row["language"], 0) + 1

    log.info("\n── Experiment Summary ──")
    log.info("Total queries run: %d", len(results_rows))
    for lang, count in sorted(by_lang.items()):
        log.info("  %s: %d queries", lang, count)

    if LANGCHAIN_TRACING:
        log.info("\nLangSmith traces: %s", project_url)
    else:
        log.info("\nLangSmith tracing was disabled. Add LANGCHAIN_API_KEY to .env to enable.")

    log.info("\nNEXT STEP: Open results/results.csv and fill in 'retrieval_correct' and 'answer_faithful' columns.")
    log.info("Then run: python analyze_results.py")
    log.info("STEP 6 complete.\n")


if __name__ == "__main__":
    main()
