"""
fetch_articles.py — Step 1
==========================
Fetches Wikipedia articles in English (en) and Hindi (hi) for 8 Indian state topics,
strips boilerplate, and saves them to data/raw/{topic}_{lang}.txt.

HALTS (does not silently substitute) if any Hindi article is missing or too short.

Run:
    python fetch_articles.py
"""

import re
import sys
import time
from pathlib import Path

import wikipediaapi
from dotenv import load_dotenv

from shared_logger import get_logger

# ─── Setup ────────────────────────────────────────────────────────────────────
load_dotenv()
log = get_logger()

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# 8 Indian states — Wikipedia page titles (English)
TOPICS: dict[str, str] = {
    "rajasthan": "Rajasthan",
    "kerala": "Kerala",
    "punjab": "Punjab, India",
    "maharashtra": "Maharashtra",
    "uttar_pradesh": "Uttar Pradesh",
    "bihar": "Bihar",
    "gujarat": "Gujarat",
    "tamil_nadu": "Tamil Nadu",
}

# Corresponding Hindi Wikipedia page titles
TOPICS_HI: dict[str, str] = {
    "rajasthan": "राजस्थान",
    "kerala": "केरल",
    "punjab": "पंजाब, भारत",
    "maharashtra": "महाराष्ट्र",
    "uttar_pradesh": "उत्तर प्रदेश",
    "bihar": "बिहार",
    "gujarat": "गुजरात",
    "tamil_nadu": "तमिल नाडु",
}

MIN_ARTICLE_LEN = 500  # characters — anything shorter is considered missing


# ─── Cleaning ─────────────────────────────────────────────────────────────────

def clean_article(text: str) -> str:
    """Strip Wikipedia boilerplate while keeping the main prose."""
    lines = text.splitlines()
    cleaned: list[str] = []
    skip_sections = {
        "see also", "references", "external links", "notes", "further reading",
        "bibliography", "gallery", "sources", "footnotes",
        "यह भी देखें", "सन्दर्भ", "बाहरी कड़ियाँ", "टिप्पणियाँ",
    }

    skipping = False
    for line in lines:
        stripped = line.strip()

        # Detect section headers like == See also ==
        header_match = re.match(r"^={2,}\s*(.+?)\s*={2,}$", stripped)
        if header_match:
            section_name = header_match.group(1).lower()
            if any(s in section_name for s in skip_sections):
                skipping = True
                log.debug("Skipping section: %s", header_match.group(1))
                continue
            else:
                skipping = False

        if skipping:
            continue

        # Drop wiki markup patterns
        if re.match(r"^\{\{.*\}\}$", stripped):          # {{template}}
            continue
        if re.match(r"^\[\[File:.*", stripped):           # [[File:...
            continue
        if re.match(r"^\[\[Image:.*", stripped):          # [[Image:...
            continue
        if re.match(r"^\|.*", stripped):                  # table cells
            continue
        if re.match(r"^!.*", stripped):                   # table headers
            continue
        if re.match(r"^thumb\|.*", stripped):             # thumb captions
            continue

        cleaned.append(line)

    result = "\n".join(cleaned)
    # Collapse 3+ consecutive blank lines to 2
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


# ─── Fetching ─────────────────────────────────────────────────────────────────

def fetch_and_save(
    wiki: wikipediaapi.Wikipedia,
    topic_key: str,
    page_title: str,
    lang: str,
) -> str:
    """Fetch a Wikipedia page, clean it, save to disk, and return the text."""
    out_path = RAW_DIR / f"{topic_key}_{lang}.txt"

    if out_path.exists() and out_path.stat().st_size > MIN_ARTICLE_LEN:
        log.info("  ✓ Already on disk: %s  (skipping fetch)", out_path.name)
        return out_path.read_text(encoding="utf-8")

    log.info("  Fetching [%s] '%s' …", lang.upper(), page_title)
    page = wiki.page(page_title)

    if not page.exists():
        log.error("  ✗ Page NOT FOUND: lang=%s title='%s'", lang, page_title)
        raise RuntimeError(f"Wikipedia page not found: [{lang}] '{page_title}'")

    raw_text = page.text
    cleaned = clean_article(raw_text)

    if len(cleaned) < MIN_ARTICLE_LEN:
        log.error(
            "  ✗ Article too short after cleaning: %d chars  (lang=%s title='%s')",
            len(cleaned), lang, page_title,
        )
        raise RuntimeError(
            f"Article too short after cleaning ({len(cleaned)} chars): "
            f"[{lang}] '{page_title}' — manual review required."
        )

    out_path.write_text(cleaned, encoding="utf-8")
    log.info(
        "  ✓ Saved %s  (%d chars)", out_path.name, len(cleaned)
    )
    return cleaned


def main() -> None:
    log.info("=" * 60)
    log.info("STEP 1 — Fetch Wikipedia Articles")
    log.info("=" * 60)

    user_agent = "hinglish-rag-diagnostic/1.0 (research@example.com)"
    wiki_en = wikipediaapi.Wikipedia(language="en", user_agent=user_agent)
    wiki_hi = wikipediaapi.Wikipedia(language="hi", user_agent=user_agent)

    errors: list[str] = []

    for topic_key, title_en in TOPICS.items():
        title_hi = TOPICS_HI[topic_key]
        log.info("\nTopic: %s", topic_key.upper())

        try:
            fetch_and_save(wiki_en, topic_key, title_en, "en")
        except RuntimeError as exc:
            log.error("FATAL: %s", exc)
            errors.append(str(exc))

        time.sleep(0.5)  # polite rate limiting

        try:
            fetch_and_save(wiki_hi, topic_key, title_hi, "hi")
        except RuntimeError as exc:
            log.error("FATAL: %s", exc)
            errors.append(str(exc))

        time.sleep(0.5)

    if errors:
        log.error("\n%d error(s) encountered — halting. Review above.", len(errors))
        for e in errors:
            log.error("  • %s", e)
        sys.exit(1)

    # Verify final file count
    txt_files = list(RAW_DIR.glob("*.txt"))
    log.info("\n── Summary ──")
    log.info("Files saved: %d / 16 expected", len(txt_files))
    for f in sorted(txt_files):
        log.info("  %s  (%d chars)", f.name, f.stat().st_size)

    if len(txt_files) < 16:
        log.warning("Expected 16 files but found %d — check above for errors.", len(txt_files))
    else:
        log.info("✓ All 16 articles fetched successfully.")

    log.info("STEP 1 complete.\n")


if __name__ == "__main__":
    main()
