import os
import subprocess
import json

PROPOSALS_FILE = "proposals.json"

def get_changed_files():
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    changed_files = []
    for line in result.stdout.splitlines():
        status, file = line[:2], line[3:]
        if status.strip() and file.endswith(".py"):
            changed_files.append(file)
    return changed_files

def commit_changes():
    changed = get_changed_files()
    if not changed:
        print("✅ No Python files changed — nothing to commit.")
        return

    subprocess.run(["git", "add"] + changed)

    try:
        with open(PROPOSALS_FILE, "r") as f:
            proposals = json.load(f)
        messages = [f"🔁 Auto-apply: {p['filename']} ({len(p['issues'])} fix{'es' if len(p['issues']) != 1 else ''})" for p in proposals]
        commit_message = "\n".join(messages)
    except:
        commit_message = "🔁 Auto-commit approved changes"

    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])
    print("🚀 Changes committed and pushed!")

if __name__ == "__main__":
    commit_changes()
