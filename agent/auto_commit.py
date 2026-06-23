import os
import sys
import time
import subprocess
from threading import Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Ensure project root is in path FIRST (critical fix)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.system_integrity import run_system_check
from agent.kernel_guard import run_kernel_check
from agent.realtime_guard import run_realtime_check
from agent.ast_kernel_guard import run_ast_kernel_check

DEBOUNCE_SECONDS = 2.5
timer = None


# -----------------------------
# GET GIT DIFF
# -----------------------------

def get_git_diff():
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True
        )

        if not result.stdout.strip():
            result = subprocess.run(
                ["git", "diff"],
                capture_output=True,
                text=True
            )

        return result.stdout

    except Exception:
        return ""


# -----------------------------
# SEMANTIC ANALYSIS ENGINE
# -----------------------------

def generate_commit_message(diff: str):
    diff_lower = diff.lower()

    tags = []

    if "router.py" in diff_lower:
        tags.append("router")

    if "kernel" in diff_lower:
        tags.append("kernel")

    if "snapshot" in diff_lower:
        tags.append("snapshot")

    if "registry" in diff_lower:
        tags.append("tools")

    if "main.py" in diff_lower:
        tags.append("core")

    if "def " in diff_lower:
        change_type = "refactor"
    elif "+" in diff and "-" in diff:
        change_type = "modify"
    elif "+" in diff:
        change_type = "add"
    elif "-" in diff:
        change_type = "remove"
    else:
        change_type = "update"

    tag_str = ", ".join(tags) if tags else "system"

    return f"{change_type}: update {tag_str}"


# -----------------------------
# GIT COMMIT
# -----------------------------

def git_commit(message):
    try:
        subprocess.run(["git", "add", "."], check=True)

        subprocess.run(
            ["git", "commit", "-m", message],
            check=True
        )

        print(f"✅ Semantic commit: {message}")

    except subprocess.CalledProcessError as e:
        print("⚠️ Commit failed:", e)


# -----------------------------
# SAFE COMMIT CHECK
# -----------------------------

def safe_commit():
    # system integrity gate
    report = run_system_check()

    if report["issues"]:
        print("🚫 Commit blocked (system integrity issues):")
        for i in report["issues"]:
            print(" -", i)
        return

    # kernel architecture gate
    kernel_report = run_kernel_check()

    if not kernel_report["ok"]:
        print("🚫 Commit blocked (kernel violations):")
        for i in kernel_report["issues"]:
            print(" -", i)
        return

    diff = get_git_diff()
    message = generate_commit_message(diff)

    git_commit(message)


# -----------------------------
# DEBOUNCE TRIGGER
# -----------------------------

def trigger_commit():
    global timer

    if timer:
        timer.cancel()

    timer = Timer(DEBOUNCE_SECONDS, safe_commit)
    timer.start()


# -----------------------------
# WATCHER
# -----------------------------

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.src_path.endswith(".py"):
            return

        print(f"🧠 Change detected: {event.src_path}")

        # 1. REAL-TIME AST CHECK (FIXED LOCATION)
        ast_check = run_ast_kernel_check(event.src_path)

        if not ast_check.get("ok", False):
            print("🚫 AST KERNEL BLOCK:")
            for i in ast_check.get("issues", []):
                print(" -", i)
            return

        # 2. continue pipeline
        trigger_commit()


def start_auto_commit():
    observer = Observer()
    observer.schedule(ChangeHandler(), path=".", recursive=True)

    observer.start()

    print("🤖 Semantic auto-commit system running...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_auto_commit()