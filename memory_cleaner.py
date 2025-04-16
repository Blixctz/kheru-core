import json
import hashlib
from difflib import SequenceMatcher

MEMORY_FILE = "memory.json"

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def hash_text(text):
    return hashlib.md5(text.strip().lower().encode()).hexdigest()

def are_similar(a, b, threshold=0.9):
    return SequenceMatcher(None, a.strip().lower(), b.strip().lower()).ratio() >= threshold

def deduplicate_memory():
    memory = load_memory()
    seen_hashes = set()
    unique_entries = []

    for entry in memory:
        val_hash = hash_text(entry["value"])

        if val_hash in seen_hashes:
            print(f"🧹 Removing exact duplicate: {entry['value'][:60]}...")
            continue

        duplicate_found = False
        for existing in unique_entries:
            if are_similar(entry["value"], existing["value"]):
                print(f"🧹 Removing near-duplicate: {entry['value'][:60]}...")
                duplicate_found = True
                break

        if not duplicate_found:
            seen_hashes.add(val_hash)
            unique_entries.append(entry)

    print(f"\n✅ Cleaned: {len(memory) - len(unique_entries)} duplicates removed.")
    save_memory(unique_entries)

if __name__ == "__main__":
    deduplicate_memory()
