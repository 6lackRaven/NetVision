import json
import os
from datetime import datetime
from data.data_handler import save_entry

LOG_PATH = "data/session.json"
IN_MEMORY_LOG = []

def log_alert(alert_text, pkt_data=None):
    timestamp = datetime.now().isoformat()
    alert_entry = {
        "time": timestamp,
        "alert": alert_text,
        "packet": pkt_data or {}
    }

    IN_MEMORY_LOG.append(alert_entry)
    print(f"[!] {timestamp} - {alert_text}")

    save_to_disk(alert_entry)

def save_to_disk(entry):
    if not os.path.exists("data"):
        os.makedirs("data")

    # Ensure the file exists
    if not os.path.isfile(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([], f)

    with open(LOG_PATH, "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecoderError:
            data = []

        data.append(entry)  # <== Moved outside the try/except block so it always runs
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()  # Optional: erase leftover data
