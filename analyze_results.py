"""
analyze_results.py — Step 8
=============================
Reads results/results.csv AFTER annotation.
Computes and prints both Topic Hit-Rate and Grounded Hit-Rate.
"""

import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from shared_logger import get_logger

matplotlib.use("Agg")
log = get_logger()

RESULTS_CSV = Path("results/results.csv")
CHART_PATH = Path("results/analysis_chart.png")

LANGUAGES = ["en", "hi", "hinglish"]
LANG_LABELS = {"en": "English", "hi": "Hindi", "hinglish": "Hinglish"}
LANG_COLORS = {"en": "#4C9EFF", "hi": "#FF6B6B", "hinglish": "#FFD166"}

def load_results() -> pd.DataFrame:
    if not RESULTS_CSV.exists():
        log.error("results.csv not found!")
        sys.exit(1)
    return pd.read_csv(RESULTS_CSV, encoding="utf-8")

def compute_rates(df: pd.DataFrame):
    topic_hit_rates = {}
    grounded_hit_rates = {}
    fai_rates = {}
    resp_counts = {"answered_grounded": [], "answered_ungrounded": [], "refused": [], "error": []}
    
    for lang in LANGUAGES:
        sub = df[df["language"] == lang]
        total = len(sub)
        if total == 0:
            topic_hit_rates[lang] = 0
            grounded_hit_rates[lang] = 0
            fai_rates[lang] = 0
            for k in resp_counts: resp_counts[k].append(0)
            continue
            
        # Topic Hit Rate
        topic_hits = 0
        for _, row in sub.iterrows():
            try:
                topics = json.loads(row["retrieved_chunk_topics"])
                if row["topic"] in topics:
                    topic_hits += 1
            except:
                pass
        
        # Grounded Hit Rate (using new auto_eval logic)
        grounded_hits = (sub["response_type"] == "answered_grounded").sum()
        
        faith_correct = (sub["answer_faithful"] == "Y").sum()
        
        topic_hit_rates[lang] = round(topic_hits / total * 100, 1)
        grounded_hit_rates[lang] = round(grounded_hits / total * 100, 1)
        fai_rates[lang] = round(faith_correct / total * 100, 1)
        
        counts = sub["response_type"].value_counts()
        resp_counts["answered_grounded"].append(counts.get("answered_grounded", 0))
        resp_counts["answered_ungrounded"].append(counts.get("answered_ungrounded", 0))
        resp_counts["refused"].append(counts.get("refused", 0))
        resp_counts["error"].append(counts.get("error", 0))
        
    return topic_hit_rates, grounded_hit_rates, fai_rates, resp_counts

def print_summary_table(df, topic_hit_rates, grounded_hit_rates, fai_rates, resp_counts):
    print("\n" + "=" * 100)
    print("SUMMARY TABLE & RESPONSE TYPE BREAKDOWN")
    print("=" * 100)
    print(f"{'Language':<12} | {'Topic Hit-Rate':<15} | {'Grounded Hit-Rate':<18} | {'Faithful':<10} | {'Grounded':<8} | {'Ungrounded':<10} | {'Refused':<8} | {'Error':<6}")
    print("-" * 100)
    
    for i, lang in enumerate(LANGUAGES):
        th = f"{topic_hit_rates[lang]:.1f}%"
        gh = f"{grounded_hit_rates[lang]:.1f}%"
        fa = f"{fai_rates[lang]:.1f}%"
        g = resp_counts["answered_grounded"][i]
        ug = resp_counts["answered_ungrounded"][i]
        ref = resp_counts["refused"][i]
        err = resp_counts["error"][i]
        
        print(f"{LANG_LABELS[lang]:<12} | {th:<15} | {gh:<18} | {fa:<10} | {g:<8} | {ug:<10} | {ref:<8} | {err:<6}")
    print("=" * 100)

def main():
    df = load_results()
    topic_hit_rates, grounded_hit_rates, fai_rates, resp_counts = compute_rates(df)
    print_summary_table(df, topic_hit_rates, grounded_hit_rates, fai_rates, resp_counts)

if __name__ == "__main__":
    main()
