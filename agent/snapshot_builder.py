import os
import json
import hashlib
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(".")
OUTPUT_FILE = Path("project_snapshot.md")
STATE_FILE = Path(".snapshot_state.json")


# -----------------------------
# UTIL: HASH FILE CONTENT
# -----------------------------
def hash_content(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# -----------------------------
# LOAD PREVIOUS STATE
# -----------------------------
def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


# -----------------------------
# COLLECT PY FILES
# -----------------------------
def collect_py_files():
    files = []
    for root, _, filenames in os.walk(PROJECT_ROOT):
        for f in filenames:
            if f.endswith(".py"):
                files.append(Path(root) / f)
    return files


# -----------------------------
# BUILD SNAPSHOT (DIFF-BASED)
# -----------------------------
def build_snapshot(kernel=None):
    state = load_state()
    new_state = {}

    snapshot = []
    snapshot.append("# PROJECT SNAPSHOT\n")
    snapshot.append(f"Generated: {datetime.now()}\n\n")

    # -------------------------
    # KERNEL SECTION
    # -------------------------
    if kernel:
        snapshot.append("## KERNEL STATE\n")
        snapshot.append("```json\n")
        snapshot.append(json.dumps(kernel, indent=2))
        snapshot.append("\n```\n\n")

    changed_files = 0

    # -------------------------
    # FILE DIFF TRACKING
    # -------------------------
    for file in collect_py_files():
        try:
            content = file.read_text(encoding="utf-8")
            file_hash = hash_content(content)

            new_state[str(file)] = file_hash

            # Only include changed files
            if state.get(str(file)) != file_hash:
                changed_files += 1

                snapshot.append(f"## FILE: {file}\n")
                snapshot.append("```python\n")
                snapshot.append(content)
                snapshot.append("\n```\n\n")

        except Exception as e:
            snapshot.append(f"## FILE: {file} (ERROR: {e})\n")

    snapshot.append("\n---\n")
    snapshot.append(f"Changed files: {changed_files}\n")

    OUTPUT_FILE.write_text("".join(snapshot), encoding="utf-8")
    save_state(new_state)

    print(f"🧠 Snapshot updated | Changed files: {changed_files}")