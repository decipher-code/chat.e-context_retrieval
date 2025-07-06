# retriever.py

import faiss
import sqlite3
import json
from sentence_transformers import SentenceTransformer
import numpy as np

# Load PubMedBERT embedder
embedder = SentenceTransformer("pritamdeka/S-PubMedBert-MS-MARCO")

# Load FAISS index & ID mapping
index = faiss.read_index("medical_faiss.index")
with open("faiss_ids.txt") as f:
    id_list = [line.strip() for line in f]

# ✅ Load boost rules from JSON
with open("boost_rules.json") as f:
    BOOST_RULES = json.load(f)

def retrieve(query: str, top_k: int = 5, min_confidence: float = 0.5):
    print(f"\n🔍 Received query: {query}")

    conn = sqlite3.connect("medical01.db")
    cur = conn.cursor()

    vec = embedder.encode([query]).astype("float32")
    vec = vec / np.linalg.norm(vec)

    distances, indices = index.search(vec, top_k)

    print(f"🧩 Distances: {distances}")
    print(f"🧩 Indices: {indices}")

    results = []
    query_lower = query.lower()

    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0:
            continue

        doc_id = id_list[idx]
        print(f"➡️ Checking ID: {doc_id}")

        disease_id, source = doc_id.split("||")
        table = "factsheets" if source == "factsheet" else "who_brief"

        row = cur.execute(
            f"SELECT id, condition, content FROM {table} WHERE id = ?",
            (disease_id,)
        ).fetchone()

        if not row:
            continue

        similarity = dist

        # ✅ Smart boosting using JSON rules
        condition_lower = row[1].lower()
        boost = 0.0

        for symptom, disease_boosts in BOOST_RULES.items():
            if symptom in query_lower:
                for disease, weight in disease_boosts.items():
                    if disease in condition_lower:
                        boost += weight

        similarity += boost

        if similarity < min_confidence:
            continue

        results.append({
            "id": row[0],
            "condition": row[1],
            "source": source,
            "content": row[2],
            "confidence": round(similarity, 4)
        })

    conn.close()
    print(f"✅ Total matches: {len(results)}\n")

    # ✅ Sort by boosted confidence
    results.sort(key=lambda x: x['confidence'], reverse=True)

    return results
