import sqlite3
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model
embedder = SentenceTransformer("pritamdeka/S-PubMedBert-MS-MARCO")

# Connect to DB
conn = sqlite3.connect("medical.db")
cur = conn.cursor()

# Load both tables
cur.execute("SELECT id, content FROM who_brief")
brief_rows = cur.fetchall()

cur.execute("SELECT id, content FROM factsheets")
factsheet_rows = cur.fetchall()

all_rows = []
for row in brief_rows:
    all_rows.append((row[0], "who_brief", row[1]))

for row in factsheet_rows:
    all_rows.append((row[0], "factsheet", row[1]))

ids = []
embeddings = []

for id, source, text in all_rows:
    emb = embedder.encode(text)
    emb = emb / np.linalg.norm(emb)   #normalize for cosine similarity
    ids.append(f"{id}||{source}")
    embeddings.append(emb)

embeddings = np.vstack(embeddings).astype('float32')

dim = embeddings.shape[1]

#  Use Inner Product index for cosine similarity
index = faiss.IndexFlatIP(dim)
index.add(embeddings)

with open("faiss_ids.txt", "w") as f:
    for id in ids:
        f.write(f"{id}\n")

faiss.write_index(index, "medical_faiss.index")

print(f"✅ FAISS index created for {len(ids)} chunks using cosine similarity!")
