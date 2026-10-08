"""
generate_queries.py — Step 4
==============================
Generates 72 query triplets (English / Hindi / Hinglish) for 8 Indian state topics.

For each topic, 3 factual English questions are hardcoded (answerable from the
Wikipedia article). Each question is then translated into Hindi (Devanagari) and
Hinglish (Romanized code-mixed) via a Groq LLM call.

Outputs:
  data/queries_for_review.csv  — all 72 queries for human sanity-check
  data/queries.json            — final structured query set

Run:
    python generate_queries.py
"""

import csv
import json
import os
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from shared_logger import get_logger

# ─── Setup ────────────────────────────────────────────────────────────────────
load_dotenv()
log = get_logger()

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

GROQ_MODEL = "openai/gpt-oss-20b"

# ─── Hardcoded English questions (factual, answer in article) ─────────────────
# 3 questions per topic × 8 topics = 24 base questions
BASE_QUESTIONS: list[dict] = [
    # Rajasthan
    {"topic": "rajasthan", "q_idx": 0, "en": "What is the capital of Rajasthan?"},
    {"topic": "rajasthan", "q_idx": 1, "en": "Which desert is located in Rajasthan?"},
    {"topic": "rajasthan", "q_idx": 2, "en": "What is the official language of Rajasthan?"},

    # Kerala
    {"topic": "kerala", "q_idx": 0, "en": "What is the capital of Kerala?"},
    {"topic": "kerala", "q_idx": 1, "en": "Which river is the longest in Kerala?"},
    {"topic": "kerala", "q_idx": 2, "en": "What is the literacy rate of Kerala known for in India?"},

    # Punjab
    {"topic": "punjab", "q_idx": 0, "en": "What is the capital of Punjab?"},
    {"topic": "punjab", "q_idx": 1, "en": "Which river gives Punjab its name?"},
    {"topic": "punjab", "q_idx": 2, "en": "What is the main language spoken in Punjab?"},

    # Maharashtra
    {"topic": "maharashtra", "q_idx": 0, "en": "What is the capital of Maharashtra?"},
    {"topic": "maharashtra", "q_idx": 1, "en": "Which dance form is famous in Maharashtra?"},
    {"topic": "maharashtra", "q_idx": 2, "en": "What is the official language of Maharashtra?"},

    # Uttar Pradesh
    {"topic": "uttar_pradesh", "q_idx": 0, "en": "What is the capital of Uttar Pradesh?"},
    {"topic": "uttar_pradesh", "q_idx": 1, "en": "Which famous monument is located in Agra, Uttar Pradesh?"},
    {"topic": "uttar_pradesh", "q_idx": 2, "en": "What is the most populated state in India?"},

    # Bihar
    {"topic": "bihar", "q_idx": 0, "en": "What is the capital of Bihar?"},
    {"topic": "bihar", "q_idx": 1, "en": "Which ancient university was located in Bihar?"},
    {"topic": "bihar", "q_idx": 2, "en": "What is the official language of Bihar?"},

    # Gujarat
    {"topic": "gujarat", "q_idx": 0, "en": "What is the capital of Gujarat?"},
    {"topic": "gujarat", "q_idx": 1, "en": "Which sea borders Gujarat on the west?"},
    {"topic": "gujarat", "q_idx": 2, "en": "What is the official language of Gujarat?"},

    # Tamil Nadu
    {"topic": "tamil_nadu", "q_idx": 0, "en": "What is the capital of Tamil Nadu?"},
    {"topic": "tamil_nadu", "q_idx": 1, "en": "Which classical dance form originated in Tamil Nadu?"},
    {"topic": "tamil_nadu", "q_idx": 2, "en": "What is the official language of Tamil Nadu?"},
]


def build_translation_prompt(english_question: str) -> str:
    return f"""You are a bilingual Indian language expert. Given an English question, produce two translations:

1. **Hindi (Devanagari script)**: A natural, accurate Hindi translation.
2. **Hinglish (Romanized code-mixed)**: How a bilingual Indian would casually type this in Roman script — mixing Hindi grammar/words with English nouns naturally. Do NOT transliterate the Hindi word-for-word into Roman letters. Write it as a real informal message, e.g. "Rajasthan ki capital kya hai" not "raajasthaan kee raajadhaanee kya hai".

English question: "{english_question}"

Respond ONLY with valid JSON (no markdown, no explanation) in this exact format:
{{
  "hindi": "<Hindi translation in Devanagari>",
  "hinglish": "<Natural Romanized Hinglish version>"
}}"""


def translate_question(client: Groq, english_question: str, retries: int = 5) -> dict[str, str]:
    """Call Groq to get Hindi + Hinglish translations. Returns dict with 'hindi' and 'hinglish' keys."""
    prompt = build_translation_prompt(english_question)

    for attempt in range(1, retries + 1):
        try:
            log.debug("  Translating (attempt %d): %s", attempt, english_question)
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500,
            )
            raw = response.choices[0].message.content or ""

            # Strip thinking blocks if any
            raw = re.sub(r"<think>[\s\S]*?</think>", "", raw, flags=re.IGNORECASE).strip()

            # Attempt regex search for JSON block
            json_match = re.search(r"\{[\s\S]*?\}", raw)
            if json_match:
                raw_json = json_match.group(0)
            else:
                raw_json = raw

            result = json.loads(raw_json)
            assert "hindi" in result and "hinglish" in result, "Missing keys"
            log.debug("    Hindi: %s", result["hindi"])
            log.debug("    Hinglish: %s", result["hinglish"])
            return result

        except (json.JSONDecodeError, AssertionError, KeyError) as exc:
            log.warning("  Parse error on attempt %d: %s — retrying…", attempt, exc)
            time.sleep(2 * attempt)
        except Exception as exc:  # noqa: BLE001
            log.warning("  API error on attempt %d: %s — retrying…", attempt, exc)
            time.sleep(3 * attempt)

    log.error("  Failed to translate after %d attempts: %s", retries, english_question)
    return {"hindi": "TRANSLATION_FAILED", "hinglish": "TRANSLATION_FAILED"}


def main() -> None:
    log.info("=" * 60)
    log.info("STEP 4 — Generate Query Triplets (English / Hindi / Hinglish)")
    log.info("=" * 60)

    groq_key = os.getenv("GROQ_API_KEY", "")
    if not groq_key or groq_key == "your_groq_api_key_here":
        log.error("GROQ_API_KEY is not set in .env — please fill it in and retry.")
        sys.exit(1)

    client = Groq(api_key=groq_key)
    log.info("Groq client initialized with model: %s", GROQ_MODEL)

    queries: list[dict] = []
    review_rows: list[dict] = []

    for bq in BASE_QUESTIONS:
        topic = bq["topic"]
        q_idx = bq["q_idx"]
        en_text = bq["en"]
        question_id = f"{topic}_q{q_idx}"

        log.info("\nTranslating: [%s] %s", question_id, en_text)

        translations = translate_question(client, en_text)
        hi_text = translations["hindi"]
        hing_text = translations["hinglish"]

        # Build the three query rows
        for lang, text in [("en", en_text), ("hi", hi_text), ("hinglish", hing_text)]:
            query_id = f"{question_id}_{lang}"
            row = {
                "query_id": query_id,
                "topic": topic,
                "question_id": question_id,
                "language": lang,
                "query_text": text,
                "expected_source_topic": topic,
            }
            queries.append(row)
            review_rows.append(
                {
                    "query_id": query_id,
                    "topic": topic,
                    "language": lang,
                    "query_text": text,
                    "naturalness_ok": "",  # human fills this in
                    "notes": "",
                }
            )

        # Polite rate limiting
        time.sleep(1.0)

    # ── Save queries_for_review.csv ──
    review_path = DATA_DIR / "queries_for_review.csv"
    fieldnames = ["query_id", "topic", "language", "query_text", "naturalness_ok", "notes"]
    with review_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(review_rows)
    log.info("\n✓ Saved review CSV: %s (%d rows)", review_path, len(review_rows))

    # ── Save queries.json ──
    queries_path = DATA_DIR / "queries.json"
    queries_path.write_text(
        json.dumps(queries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log.info("✓ Saved queries.json: %s (%d queries)", queries_path, len(queries))

    # Verify count
    expected = len(BASE_QUESTIONS) * 3  # 24 × 3 = 72
    if len(queries) != expected:
        log.warning("Expected %d queries but generated %d!", expected, len(queries))
    else:
        log.info("✓ Query count correct: %d (8 topics × 3 questions × 3 languages)", len(queries))

    log.info("STEP 4 complete.\n")
    log.info("ACTION REQUIRED: Review data/queries_for_review.csv for Hinglish naturalness")
    log.info("Then run: python run_experiment.py")


if __name__ == "__main__":
    main()
