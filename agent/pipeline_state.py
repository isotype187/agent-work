import os
import json
import time


STATE_FILE = "memory/pipeline_state.json"


def _load():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "state": "CLEAN",
            "last_update": None
        }


def _save(data):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_state():
    return _load().get("state", "CLEAN")


def set_state(new_state: str):
    data = _load()

    data["state"] = new_state
    data["last_update"] = time.time()

    _save(data)


def snapshot():
    return _load()