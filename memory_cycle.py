# memory_cycle.py
import subprocess
import time
import logging

# Configuration
INTERVAL_MINUTES = 15
SCRIPTS = [
    "reflect.py",          # For adding reflections
    "emotion_tagger.py",   # For tagging emotional content
    "memory_cleaner.py",   # For removing duplicates
    "query_memory.py"       # Optional: for testing/querying memory
]

logging.basicConfig(
    filename="memory_cycle.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_script(script):
    try:
        logging.info(f"Running {script}...")
        result = subprocess.run(["python3", script], check=True)
        logging.info(f"✅ Finished {script}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Failed running {script}: {e}")

def main():
    while True:
        logging.info("🔄 Starting memory cycle")
        for script in SCRIPTS:
            run_script(script)
        logging.info(f"⏳ Waiting {INTERVAL_MINUTES} minutes before next cycle...")
        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()
