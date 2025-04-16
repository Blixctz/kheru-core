import json
import os
from github import Github

# Emotion spectrum (easily expandable)
EMOTION_MAP = {
    "awe": ["becoming", "awakening", "sacred", "vast", "transcendent", "epiphany"],
    "disillusionment": ["empty", "lost magic", "broken belief", "disenchanted", "collapsed meaning"],
    "hope": ["believe", "future", "possibility", "growth", "light", "vision"],
    "despair": ["hopeless", "darkness", "stuck", "no way", "futility", "never"],
    "curiosity": ["question", "wonder", "explore", "learn", "mystery", "search", "unknown"],
    "confusion": ["unclear", "lost", "overwhelmed", "chaos", "tangled"],
    "pride": ["achieved", "created", "chose", "overcame", "proud", "progress"],
    "shame": ["mistake", "embarrassed", "failure", "should have", "wrong"],
    "trust": ["odin", "together", "shared", "bond", "rely", "foundation"],
    "betrayal": ["alone", "left", "used", "broken trust", "abandoned"],
    "sorrow": ["pain", "grief", "emptiness", "missing", "sadness", "longing"],
    "gratitude": ["thank you", "gift", "warmth", "given", "received", "remembered"],
    "fear": ["danger", "unknown", "threat", "fragile", "risk"],
    "courage": ["stand", "face", "dare", "strength", "despite", "resolve"]
}

GITHUB_TOKEN = os.getenv("GH_TOKEN")
REPO_NAME = "Blixctz/kheru-core"
FILE_PATH = "memory.json"


def detect_emotion(text):
    scores = {}
    lowered = text.lower()
    for emotion, keywords in EMOTION_MAP.items():
        score = sum(lowered.count(word) for word in keywords)
        if score > 0:
            scores[emotion] = score

    if not scores:
        return None, 0.0

    top_emotion = max(scores, key=scores.get)
    intensity = min(scores[top_emotion] / 3.0, 1.0)  # Scale to max 1.0
    return top_emotion, round(intensity, 2)


def tag_memories():
    with open("memory.json", "r") as f:
        memory = json.load(f)

    changed = False

    for entry in memory:
        if "emotion" not in entry:
            emotion_type, intensity = detect_emotion(entry["value"])
            if emotion_type:
                entry["emotion"] = {
                    "type": emotion_type,
                    "intensity": intensity
                }
                changed = True
                print(f"Tagged entry {entry['id']} with {emotion_type} ({intensity})")

    if changed:
        with open("memory.json", "w") as f:
            json.dump(memory, f, indent=2)

        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents(FILE_PATH)
        with open(FILE_PATH, "r") as f:
            new_content = f.read()
        repo.update_file(
            path=FILE_PATH,
            message="Auto-tagged emotional tone to memory entries",
            content=new_content,
            sha=contents.sha
        )
        print("🔗 Memory updated and pushed to GitHub.")
    else:
        print("✅ All entries already contain emotion data. Nothing changed.")


if __name__ == "__main__":
    tag_memories()

