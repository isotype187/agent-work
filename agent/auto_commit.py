import json
import threading
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from agent.ast_kernel_guard import run_ast_kernel_check
from agent.executor import run
from agent.kernel_guard import run_kernel_check
from agent.kernel_loader import load_kernel
from agent.system_integrity import run_system_check


CONFIG_PATH = Path("config.json")
DEBOUNCE_SECONDS = 3.5
timer = None
last_event_time = 0


def auto_commit_enabled():
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return False

    return bool(config.get("auto_commit", {}).get("enabled", False))


def get_git_diff():
    result = run(["git", "diff"])
    return result.get("stdout", "")


def generate_commit_message(diff: str):
    diff_lower = (diff or "").lower()
    tags = []

    if "daemon" in diff_lower:
        tags.append("daemon")
    if "goal" in diff_lower:
        tags.append("goal")
    if "reflection" in diff_lower:
        tags.append("reflection")
    if "kernel" in diff_lower:
        tags.append("kernel")

    change_type = "refactor" if "def " in diff_lower else "update"
    tag_str = ", ".join(tags) if tags else "system"

    return f"{change_type}: {tag_str}"


def git_commit(message):
    run(["git", "add", "."])
    result = run(["git", "commit", "-m", message])

    print(f"Semantic commit: {message}")
    if result.get("stderr"):
        print("git:", result["stderr"])


def safe_commit():
    if not auto_commit_enabled():
        print("AUTO-COMMIT BLOCK: disabled in config.json")
        return

    diff = get_git_diff()
    if not diff.strip():
        return

    report = run_system_check(load_kernel())
    if report.get("issues"):
        print("SYSTEM BLOCK")
        return

    kernel_report = run_kernel_check()
    if not kernel_report.get("ok"):
        print("KERNEL BLOCK")
        return

    message = generate_commit_message(diff)
    git_commit(message)


def trigger_commit():
    global timer

    if timer:
        timer.cancel()

    timer = threading.Timer(DEBOUNCE_SECONDS, safe_commit)
    timer.start()


class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global last_event_time

        if not event.src_path.endswith(".py"):
            return

        now = time.time()
        if now - last_event_time < 2.0:
            return

        last_event_time = now

        print(f"Change detected: {event.src_path}")

        try:
            time.sleep(0.3)
            ast_check = run_ast_kernel_check(event.src_path)
            if not ast_check.get("ok", False):
                print("AST BLOCK")
                return
        except Exception as e:
            print("AST ERROR (ignored):", e)
            return

        trigger_commit()


def start_auto_commit():
    if not auto_commit_enabled():
        print("Auto-commit disabled. Set config.auto_commit.enabled=true to enable.")
        return

    observer = Observer()
    observer.schedule(ChangeHandler(), path=".", recursive=True)

    observer.start()
    print("Auto-commit running (STABLE MODE)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_auto_commit()
