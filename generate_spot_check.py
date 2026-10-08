import pandas as pd
import json
import random

df = pd.read_csv("results/results.csv", encoding="utf-8")

# Load chunks text map
chunks_map = {}
with open("results/retrieved_chunks.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        text_lines = []
        for i, c in enumerate(data["top_3_chunks"]):
            text_lines.append(f"**Chunk {i+1} (Topic: {c['topic']}, Lang: {c['chunk_language']}):**\n{c['chunk_text']}\n")
        chunks_map[data["query_id"]] = "\n".join(text_lines)

# Select 15 rows:
# Priority 1: retrieval_correct == 'N'
# Priority 2: response_type == 'answered_ungrounded'
# Priority 3: random mix of others

# Filter categories
ungrounded = df[df['response_type'] == 'answered_ungrounded'].copy()
retrieval_n = df[df['retrieval_correct'] == 'N'].copy()

# Avoid duplicates in our priority sets
priority_df = pd.concat([ungrounded, retrieval_n]).drop_duplicates()

# Rest of the data
rest_df = df[~df['query_id'].isin(priority_df['query_id'])].copy()

# Sample
n_priority = len(priority_df)
if n_priority >= 15:
    sampled_df = priority_df.sample(n=15, random_state=42)
else:
    # Take all priority ones, and pad with rest
    sampled_df = pd.concat([priority_df, rest_df.sample(n=15 - n_priority, random_state=42)])

# Write to markdown
with open("results/spot_check.md", "w", encoding="utf-8") as f:
    f.write("# RAG Diagnostic - Manual Spot Check\n\n")
    f.write("Please review the following 15 rows. Add `CONFIRM` or `CORRECT-TO-X` next to each row.\n\n")
    
    for idx, row in sampled_df.iterrows():
        qid = row['query_id']
        f.write(f"## Query ID: {qid}\n")
        f.write(f"**Language**: {row['language']}\n\n")
        f.write(f"**Query**: {row['query_text']}\n\n")
        
        f.write("### Retrieved Context (Top 3 Chunks)\n")
        f.write(chunks_map.get(qid, "No chunks found."))
        f.write("\n")
        
        f.write(f"### Generated Answer\n> {row['generated_answer']}\n\n")
        
        f.write("### Automated Labels\n")
        f.write(f"- **retrieval_correct**: {row['retrieval_correct']}\n")
        f.write(f"- **answer_faithful**: {row['answer_faithful']}\n")
        f.write(f"- **response_type**: {row['response_type']}\n")
        f.write("\n---\n\n")

print("Generated results/spot_check.md with 15 rows for manual review.")
