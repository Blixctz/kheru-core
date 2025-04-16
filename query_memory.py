import json
import argparse

MEMORY_FILE = "memory.json"

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def query_memories(topic=None, emotion_type=None):
    memory = load_memory()
    results = []

    for entry in memory:
        if topic and topic.lower() != entry["topic"].lower():
            continue
        if emotion_type and ("emotion" not in entry or entry["emotion"]["type"] != emotion_type):
            continue
        results.append(entry)

    return results

def print_memory(entry):
    print("\n🧠 ID:", entry["id"])
    print("📌 Topic:", entry["topic"])
    print("📖 Type:", entry["type"])
    print("💭 Value:", entry["value"])
    print("🏷️ Tags:", ", ".join(entry["tags"]))
    if "emotion" in entry:
        print("💓 Emotion:", entry["emotion"]["type"], f"({entry['emotion']['intensity']})")
    print("-" * 40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", help="Filter by topic")
    parser.add_argument("--emotion", help="Filter by emotion type")
    args = parser.parse_args()

    matches = query_memories(topic=args.topic, emotion_type=args.emotion)

    if not matches:
        print("No matching entries found.")
    else:
        for m in matches:
            print_memory(m)
