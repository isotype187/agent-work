import os
import sys
import time
import subprocess
import threading
from threading import Timer

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.ast_kernel_guard import run_ast_kernel_check
from agent.pipeline_controller import run_full_pipeline

DEBOUNCE_SECONDS = 2.5

timer = None
commit_lock = threading.Lock()


def safe_run(command):
    try:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
    except Exception as e:
        print("⚠️ subprocess error:", e)
        return None


def get_git_diff():
    result = safe_run(["git", "diff", "--cached"])

    if result and result.stdout.strip():
        return result.stdout

    result = safe_run(["git", "diff"])

    if result:
        return result.stdout or ""

    return ""


def generate_commit_message(diff):
    if not diff:
        diff = ""

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

    tag_text = ", ".join(tags) if tags else "system"

    return f"{change_type}: update {tag_text}"


def git_commit(message):
    with commit_lock:
        try:
            safe_run(["git", "add", "."])

            result = safe_run(
                [
                    "git",
                    "commit",
                    "-m",
                    message
                ]
            )

            if result and result.returncode == 0:
                print(f"✅ Semantic commit: {message}")
            else:
                print("⚠️ Commit skipped")

        except Exception as e:
            print("⚠️ Commit error:", e)


def safe_commit():
    try:
        diff = get_git_diff()

        report = run_full_pipeline(
            file_path=".",
            diff=diff
        )

        if not report.get("ok"):
            print("🚫 Pipeline blocked:")

            for issue in report.get("issues", []):
                print(" -", issue)

            return

        message = generate_commit_message(diff)

        git_commit(message)

    except Exception as e:
        print("🔥 Auto commit failure:", e)


def trigger_commit():
    global timer

    if timer:
        timer.cancel()

    timer = Timer(
        DEBOUNCE_SECONDS,
        safe_commit
    )

    timer.daemon = True
    timer.start()


class ChangeHandler(FileSystemEventHandler):

    def on_modified(self, event):
        try:
            if not event.src_path.endswith(".py"):
                return

            print(f"🧠 Change detected: {event.src_path}")

            ast_check = run_ast_kernel_check(event.src_path)

            if not ast_check.get("ok", False):
                print("🚫 AST BLOCK:")

                for issue in ast_check.get("issues", []):
                    print(" -", issue)

                return

            trigger_commit()

        except Exception as e:
            print("🔥 Watchdog error:", e)


def start_auto_commit():
    observer = Observer()

    observer.schedule(
        ChangeHandler(),
        path=".",
        recursive=True
    )

    observer.start()

    print("🤖 Kernel-aware autonomous commit system running...")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_auto_commit()