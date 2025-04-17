import time
import subprocess
import os
import logging
from failsafe import verify_integrity

INTERVAL_MINUTES = 30
PROPOSALS_FILE = "proposals.json"

logging.basicConfig(filename="cycle.log", level=logging.INFO)

def run(command):
    try:
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            logging.error(f"Command failed: {command}")
    except Exception as e:
        logging.error(f"Error running command: {command} — {e}")

def proposals_pending():
    return os.path.exists(PROPOSALS_FILE) and os.path.getsize(PROPOSALS_FILE) > 0

def main():
    logging.info("🔄 Self-looping cycle started.")
    while True:
        logging.info("⏳ Sleeping until next cycle...")
        time.sleep(INTERVAL_MINUTES * 60)

        if not verify_integrity():
            logging.critical("❌ Failsafe triggered. Shutting down self-loop.")
            break

        logging.info("🔍 Beginning self-scan...")
        run("python3 self_editor.py")

        if proposals_pending():
            logging.info("🛑 Proposals found. Awaiting manual approval before continuing.")
            while proposals_pending():
                time.sleep(60)
            logging.info("✅ Approval complete. Continuing loop.")

        run("python3 auto_committer.py")

if __name__ == "__main__":
    main()
