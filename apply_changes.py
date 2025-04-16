import json
import os
import difflib

PROPOSALS_FILE = "proposals.json"

def load_proposals():
    if not os.path.exists(PROPOSALS_FILE):
        print("❌ proposals.json not found.")
        return []

    with open(PROPOSALS_FILE, "r") as f:
        return json.load(f)

def review_proposals(proposals):
    for proposal in proposals:
        filename = proposal["filename"]
        issues = proposal["issues"]
        new_code = proposal["proposed_code"]

        print(f"\n📂 File: {filename}")
        print("❓ Issues:")
        for issue in issues:
            print(f"   - {issue}")

        if not os.path.exists(filename):
            print("⚠️  File does not exist — will create new.")
            original_code = ""
        else:
            with open(filename, "r") as f:
                original_code = f.read()

        diff = difflib.unified_diff(
            original_code.splitlines(),
            new_code.splitlines(),
            fromfile="original",
            tofile="proposed",
            lineterm=""
        )
        print("\n🔍 Diff Preview:")
        for line in diff:
            print(line)

        choice = input("\n💡 Apply this change? (Y/n): ").strip().lower()
        if choice in ("", "y", "yes"):
            with open(filename, "w") as f:
                f.write(new_code)
            print(f"✅ Applied changes to {filename}")
        else:
            print("⏭️  Skipped.")

# Start the process
if __name__ == "__main__":
    proposals = load_proposals()
    if not proposals:
        print("No proposals to apply.")
    else:
        print(f"✅ Loaded {len(proposals)} proposal(s).")
        review_proposals(proposals)
