import os
import sys
import time
from threading import Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from agent.ast_kernel_guard import run_ast_kernel_check
from agent.console import configure_console_encoding
from agent.pipeline_controller import run_full_pipeline
from agent.runtime import safe_run

configure_console_encoding()


DEBOUNCE_SECONDS = 2.5
timer = None


def get_git_diff():
    try:
        result = safe_run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True
        )

        if not result["stdout"].strip():
            result = safe_run(
                ["git", "diff"],
                capture_output=True,
                text=True
            )

        return result["stdout"]
    except Exception:
        return ""


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


def git_commit(message):
    try:
        safe_run(["git", "add", "."], check=True)
        safe_run(["git", "commit", "-m", message], check=True)
        print(f"✅ Semantic commit: {message}")
    except Exception as e:
        print("⚠️ Commit failed:", e)


def safe_commit():

    report = run_full_pipeline(
        file_path=".",
        diff=get_git_diff()
    )

    state = report.get("state")

    if not report["ok"]:
        print(f"🚫 STATE: {state}")

        print("PIPELINE BLOCKED:")

        for issue in report["issues"]:
            print(" -", issue)

        if report.get("healing"):
            print("\n🛠 HEALING:")
            for repair in report["healing"].get("repairs", []):
                print(" →", repair["suggested_fix"])

        return

    print(f"🟢 STATE: {state}")

    git_commit(generate_commit_message(get_git_diff()))


def trigger_commit():
    global timer

    if timer:
        timer.cancel()

    timer = Timer(DEBOUNCE_SECONDS, safe_commit)
    timer.start()


class ChangeHandler(FileSystemEventHandler):

    def on_modified(self, event):

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


def start_auto_commit():
    observer = Observer()
    observer.schedule(ChangeHandler(), path=".", recursive=True)
    observer.start()

    print("🤖 STATE MACHINE AUTO-COMMIT RUNNING...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_auto_commit()
