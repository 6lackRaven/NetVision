import json
import os
from datetime import datetime

SESSION_FILE = os.path.join(os.path.dirname(__file__), "session.json")

def save_entry(entry):
    """Append a new log entry to session.json"""

    try:
        # Create the file if it doesn't exist
        if not os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "w") as f:
                json.dump([], f, indent=4)

        # Read existing data
        with open(SESSION_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

        # Add timestamp and new entry
        entry["timestamp"] = datetime.utcnow().isoformat()
        data.append(entry)

        # Save updated data
        with open(SESSION_FILE, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print(f"[DATA][ERROR] Could not save log: {e}")
