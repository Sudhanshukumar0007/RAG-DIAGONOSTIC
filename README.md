# Hinglish vs Hindi vs English — RAG Diagnostic Experiment

A small diagnostic that tests whether a **vanilla RAG pipeline** degrades in retrieval quality and answer faithfulness when queried in **Romanized Hindi-English code-mixed text ("Hinglish")**, compared to the same content queried in pure **English** or pure **Hindi (Devanagari)**.

---

## Setup

### 1. Create and activate the virtual environment (Python 3.10)

```bash
# Create venv with Python 3.10
py -3.10 -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.\venv\Scripts\activate.bat

# Activate (macOS/Linux)
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> The embedding model (`paraphrase-multilingual-MiniLM-L12-v2`) is ~500 MB and will be downloaded on first `build_index.py` run.

### 2. Fill in your API keys

Open `.env` and replace the placeholder values:

```
GROQ_API_KEY=gsk_...        # https://console.groq.com/keys
LANGCHAIN_API_KEY=ls__...   # https://smith.langchain.com/settings  (optional but recommended)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=hinglish-rag-diagnostic
```

> **LangSmith is optional** — if you leave `LANGCHAIN_API_KEY` as a placeholder, tracing is skipped and the `langsmith_trace_url` column in results.csv will say `tracing_disabled`.

---

## Run Order

### Step 1 — Fetch Wikipedia articles

```bash
python fetch_articles.py
```

Fetches 8 Indian state articles in both English and Hindi, strips boilerplate, saves to `data/raw/`.  
**Halts** if any Hindi article is missing or too short — does not silently substitute.

Expected output: `data/raw/` with 16 `.txt` files.

---

### Step 2+3 — Build vector index

```bash
python build_index.py
```

- Chunks all articles (`chunk_size=500`, `chunk_overlap=50`)
- Embeds with `paraphrase-multilingual-MiniLM-L12-v2`
- Stores in Chroma at `./chroma_db/`
- **Idempotent**: if Chroma already has data, skips re-embedding (delete `./chroma_db/` to force rebuild)

Prints embedding model name and dimension. Saves model info to `data/embedding_model_info.json`.

---

### Step 4 — Generate query triplets

```bash
python generate_queries.py
```

- Uses hardcoded 24 English questions (3 per topic)
- Calls Groq (`qwen/qwen3-32b`) to produce Hindi + Hinglish versions of each
- Saves `data/queries_for_review.csv` for human sanity-check

**⚠️ ACTION REQUIRED**: Open `data/queries_for_review.csv` and check that the Hinglish column looks natural (informal, code-mixed, NOT word-for-word transliteration). Fill in `naturalness_ok` column if you like.

Final query set saved to `data/queries.json` (72 queries).

---

### Step 5+6 — Run the experiment

```bash
python run_experiment.py
```

Runs all 72 queries through the LangGraph pipeline:
- `retrieve` node: embed query → Chroma top-5 → attach metadata + similarity scores
- `generate` node: RAG prompt → Groq → answer

Writes:
- `results/results.csv` — one row per query with 2 blank annotation columns
- `results/retrieved_chunks.jsonl` — top-3 full chunk texts per query (use this during annotation)

If LangSmith is configured, every run is traced automatically.

---

### Step 7 — Manual annotation

Open `results/results.csv` and fill in:

| Column | Values | Meaning |
|---|---|---|
| `retrieval_correct` | `Y` / `N` | Was the correct topic's chunk in the top-5? |
| `answer_faithful` | `Y` / `N` / `hallucinated` | Is the answer supported by the retrieved context? |

Use `results/retrieved_chunks.jsonl` to read the full chunk text alongside the answer — much easier than cross-referencing chunk IDs.

**Note**: Faithfulness is independent of factual accuracy — judge whether the answer follows from the retrieved context, not whether it's true in reality.

---

### Step 8 — Analyze results

```bash
python analyze_results.py
```

Computes:
- Retrieval hit-rate (%) by language
- Faithfulness rate (%) by language
- Hinglish wrong-retrieval breakdown (which language/topic chunks were retrieved instead)

Saves bar chart to `results/analysis_chart.png`.

---

## File Structure

```
.
├── .env                             # API keys (fill in before running)
├── requirements.txt
├── shared_logger.py                 # shared rotating logger (all scripts use this)
├── fetch_articles.py                # Step 1
├── build_index.py                   # Steps 2+3
├── generate_queries.py              # Step 4
├── pipeline.py                      # LangGraph graph definition (Steps 5+6)
├── run_experiment.py                # Step 6 runner
├── analyze_results.py               # Step 8
├── logs/
│   └── experiment.log               # all steps logged here
├── data/
│   ├── raw/                         # 16 Wikipedia article .txt files
│   │   ├── rajasthan_en.txt
│   │   ├── rajasthan_hi.txt
│   │   └── ...
│   ├── embedding_model_info.json    # model name + dimension
│   ├── queries_for_review.csv       # human sanity-check file
│   └── queries.json                 # 72 structured queries
├── chroma_db/                       # persisted Chroma vector index
└── results/
    ├── results.csv                  # per-query results + annotation cols
    ├── retrieved_chunks.jsonl       # top-3 chunk texts per query
    └── analysis_chart.png           # bar chart (after analyze_results.py)
```

---

## Design Notes

### Why a single shared index?
All English and Hindi chunks are stored in one Chroma collection to mirror a real-world knowledge base that isn't cleanly separated by language. This is what creates the cross-script retrieval challenge.

### Why no query rewriting / reranking?
This is a **vanilla RAG baseline** — the whole point is to measure unmodified retrieval behavior. Any augmentation would confound the language comparison.

### Embedding model
`paraphrase-multilingual-MiniLM-L12-v2` supports 50+ languages including Hindi, but was trained primarily on Latin-script text. Hinglish (Romanized Hindi) is an out-of-distribution input for it, which is exactly the degradation we're testing.

### LLM
`qwen/qwen3-32b` via Groq is used for both query translation (Step 4) and answer generation (Step 6).

### LangSmith tracing
Configure via `.env`. The trace URL in `results.csv` points to the project-level dashboard; individual run traces are searchable by `run_name` (set to the `query_id`).
# RAG-DIAGONOSTIC
