import json
import os
import hashlib

USERS_FILE = "users.json"
HISTORY_DIR = "user_history"  # directory to store per-user history JSON files

def load_user_data():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_data(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------- User History --------------------
def load_user_history(email):
    """
    Load a list of the user's past detections.
    Each entry: {"name": ..., "image_path": ..., "summary_path": ..., "timestamp": ...}
    Remove entries where the image or summary file is missing.
    """
    history_file = os.path.join(HISTORY_DIR, f"{email}.json")
    valid_history = []

    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                history = json.load(f)
        except Exception:
            history = []

        for record in history:
            image_exists = record.get("image_path") and os.path.exists(record["image_path"])
            summary_exists = record.get("summary_path") and os.path.exists(record["summary_path"])
            if image_exists and summary_exists:
                valid_history.append(record)

        # Save filtered history back to file
        with open(history_file, "w") as f:
            json.dump(valid_history, f, indent=4)

    return valid_history


def save_user_history(email, record):
    """
    Append a new detection record to the user's history.
    `record` should be a dict: {"name": ..., "image_path": ..., "summary_path": ..., "timestamp": ...}
    """
    os.makedirs(HISTORY_DIR, exist_ok=True)
    history_file = os.path.join(HISTORY_DIR, f"{email}.json")
    history = []

    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                history = json.load(f)
        except Exception:
            history = []

    history.append(record)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)
