import os
import json

INPUT_DIR = "separated jsons/who_diseases"
OUTPUT_FILE = "merged_who_diseases.json"

all_diseases = {}

for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".json"):
        filepath = os.path.join(INPUT_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                disease_name = os.path.splitext(filename)[0]
                all_diseases[disease_name] = data
            except json.JSONDecodeError as e:
                print(f"[ERROR] Failed to read {filename}: {e}")

# Save merged file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_diseases, f, indent=2, ensure_ascii=False)

print(f"[DONE] Merged {len(all_diseases)} files into {OUTPUT_FILE}")
