import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
PROPOSALS_FILE = "proposals.json"
RAW_RESPONSES_DIR = os.path.join(REPO_DIR, "raw_responses")
os.makedirs(RAW_RESPONSES_DIR, exist_ok=True)

def get_python_files():
    return [f for f in os.listdir(REPO_DIR) if f.endswith(".py") and f != os.path.basename(__file__)]

def extract_json(text):
    try:
        match = re.search(r"\{.*\}\s*\Z", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in response")

        raw_json = match.group(0)

        def sanitize_code(code):
            return code.replace("\n", "\\n").replace("\"", "\\\"")

        raw_json = re.sub(
            r'("proposed_code"\s*:\s*")(.*?)"\s*,?',
            lambda m: f'{m.group(1)}{sanitize_code(m.group(2))}"',
            raw_json,
            flags=re.DOTALL
        )

        return json.loads(raw_json)
    except Exception as e:
        print(f"❗ JSON extraction failed: {e}")
        return None

def analyze_file(filename):
    with open(os.path.join(REPO_DIR, filename), "r") as f:
        code = f.read()

    prompt = f"""
You are a self-editing AI named Kheru. Your job is to analyze the following Python script and suggest improvements or corrections.
ONLY return a JSON object with the following fields:
  - filename: the name of the file
  - issues: a list of short descriptions of what's wrong or could be improved
  - proposed_code: a complete REPLACEMENT for the current code (as a single string)

Do NOT explain, narrate, or include markdown code blocks.
Return ONLY the raw JSON.

Example:
{{
  "filename": "example.py",
  "issues": ["Too many print statements", "Lacks error handling"],
  "proposed_code": "import os\\nprint(\"Improved!\")"
}}

Filename: {filename}
Code:
{code}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Kheru, an AI that returns JSON-only code suggestions. Never explain unless explicitly asked."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()
    print(f"\n📤 Raw response from GPT-4 for {filename}:")
    print(content[:500] + ("..." if len(content) > 500 else ""))

    with open(os.path.join(RAW_RESPONSES_DIR, f"{filename}.txt"), "w") as raw_file:
        raw_file.write(content)

    data = extract_json(content)
    if data:
        return data
    else:
        print(f"❗ Could not parse a JSON proposal from {filename}.")
        return None

def write_proposals(proposals):
    with open(os.path.join(REPO_DIR, PROPOSALS_FILE), "w") as f:
        json.dump(proposals, f, indent=2)

def main():
    all_proposals = []
    py_files = get_python_files()

    print("🔍 Scanning for improvements...")
    for file in py_files:
        result = analyze_file(file)
        if result:
            print(f"📝 Suggestions found for {file} — {len(result['issues'])} issue(s)")
            all_proposals.append(result)
        else:
            print(f"✅ No actionable issues found in {file}")

    if all_proposals:
        write_proposals(all_proposals)
        print(f"💾 Proposals written to {PROPOSALS_FILE}")
    else:
        print("🎉 All files are clean — no proposals generated.")

if __name__ == "__main__":
    main()
