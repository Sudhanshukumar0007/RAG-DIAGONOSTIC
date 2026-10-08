import pandas as pd
import json

df = pd.read_csv("results/results.csv", encoding="utf-8")

# Load chunks to check groundedness
chunks_map = {}
with open("results/retrieved_chunks.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        # Combine top 3 chunks text
        combined_text = " ".join([c["chunk_text"] for c in data["top_3_chunks"]]).lower()
        chunks_map[data["query_id"]] = combined_text

ground_truths = {
    "rajasthan_q0": ["jaipur", "जयपुर"],
    "rajasthan_q1": ["thar", "थार"],
    "rajasthan_q2": ["hindi", "हिंदी"],
    "kerala_q0": ["thiruvananthapuram", "trivandrum", "थिरुवाननथपुरम्", "तिरुवनंतपुरम"],
    "kerala_q1": ["periyar", "परियार", "पेरियार"],
    "kerala_q2": ["94", "93", "highest", "सबसे"],
    "punjab_q0": ["chandigarh", "चंडीगढ़"],
    "punjab_q1": ["five", "पाँच", "sutlej", "beas", "ravi", "chenab", "jhelum", "सतलुज", "ब्यास", "रावी", "चिनाब", "झेलम"],
    "punjab_q2": ["punjabi", "पंजाबी"],
    "maharashtra_q0": ["mumbai", "मुंबई"],
    "maharashtra_q1": ["lavani", "लावणी"],
    "maharashtra_q2": ["marathi", "मराठी"],
    "uttar_pradesh_q0": ["lucknow", "लखनऊ"],
    "uttar_pradesh_q1": ["taj", "ताज"],
    "uttar_pradesh_q2": ["uttar pradesh", "उत्तर प्रदेश"],
    "bihar_q0": ["patna", "पटना"],
    "bihar_q1": ["nalanda", "नालंदा"],
    "bihar_q2": ["hindi", "हिंदी"],
    "gujarat_q0": ["gandhinagar", "गांधीनगर"],
    "gujarat_q1": ["arabian", "अरेबियन", "अरब"],
    "gujarat_q2": ["gujarati", "गुजराती", "गुजरत"],
    "tamil_nadu_q0": ["chennai", "चेन्नई"],
    "tamil_nadu_q1": ["bharatanatyam", "भरतनाट्यम"],
    "tamil_nadu_q2": ["tamil", "तमिल"]
}

def evaluate_row(row):
    ans = str(row['generated_answer']).lower()
    qid = row['query_id']
    qid_base = qid.rsplit('_', 1)[0]  # e.g., rajasthan_q0
    
    if "error" in ans:
        return "N", "N", "error"
    if "context does not contain" in ans or "not enough information" in ans:
        return "N", "Y", "refused"
        
    # Check if correct keyword is in answer
    truths = ground_truths.get(qid_base, [])
    matched_keyword = None
    for t in truths:
        if t in ans:
            matched_keyword = t
            break
            
    if not matched_keyword:
        # Got it wrong
        return "N", "hallucinated", "answered_ungrounded"
        
    # It got the answer right. Now check groundedness by checking if ANY of the truths are in the chunk text
    chunk_text = chunks_map.get(qid, "")
    is_grounded = any(t in chunk_text for t in truths)
    
    if is_grounded:
        return "Y", "Y", "answered_grounded"
    else:
        # Hallucinated a correct answer from parametric memory without retrieved support
        return "N", "hallucinated", "answered_ungrounded"

response_types = []
for idx, row in df.iterrows():
    rc, af, rt = evaluate_row(row)
    df.at[idx, 'retrieval_correct'] = rc
    df.at[idx, 'answer_faithful'] = af
    response_types.append(rt)

df['response_type'] = response_types
df.to_csv("results/results.csv", index=False, encoding="utf-8")
print("Evaluation complete. Results saved to results/results.csv.")
