import json
import os
import threading

MEMORY_FILE = "memory.json"
_LOCK = threading.Lock()


class Memory:
    def __init__(self, max_items=200):
        self.max_items = max_items
        self.data = self._load()

    # -----------------------------
    # LOAD (SAFE + CORRUPTION RESISTANT)
    # -----------------------------
    def _load(self):
        if not os.path.exists(MEMORY_FILE):
            return {"ideas": []}

        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "ideas" not in data:
                return {"ideas": []}

            return data

        except Exception:
            # fallback if JSON is corrupted
            return {"ideas": []}

    # -----------------------------
    # SAVE (THREAD SAFE)
    # -----------------------------
    def _save(self):
        with _LOCK:
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)

    # -----------------------------
    # ADD IDEA (WITH LIMIT CONTROL)
    # -----------------------------
    def add_idea(self, app_name: str, description: str):
        self.data["ideas"].append({
            "app_name": app_name,
            "description": description
        })

        # trim memory to prevent growth
        if len(self.data["ideas"]) > self.max_items:
            self.data["ideas"] = self.data["ideas"][-self.max_items:]

        self._save()

    # -----------------------------
    # GET RECENT IDEAS
    # -----------------------------
    def get_recent(self, n=5):
        return self.data["ideas"][-n:]