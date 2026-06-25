import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from agent.ast_kernel_guard import run_ast_kernel_check
from agent.system_integrity import run_system_check
from agent.kernel_guard import run_kernel_check
from agent.executor import run  # 🔥 unified subprocess layer


DEBOUNCE_SECONDS = 3.5
timer = None
last_event_time = 0


# -----------------------------
# SAFE GIT DIFF (FIXED)
# -----------------------------
def get_git_diff():
    result = run(["git", "diff"])
    return result.get("stdout", "")


# -----------------------------
# COMMIT MESSAGE
# -----------------------------
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


# -----------------------------
# COMMIT EXECUTION (FIXED)
# -----------------------------
def git_commit(message):
    run(["git", "add", "."])
    result = run(["git", "commit", "-m", message])

    print(f"✅ Semantic commit: {message}")
    if result.get("stderr"):
        print("ℹ️ git:", result["stderr"])


# -----------------------------
# SAFE COMMIT (STABLE)
# -----------------------------
def safe_commit():
    diff = get_git_diff()

    if not diff.strip():
        return

    report = run_system_check()
    if report.get("issues"):
        print("🚫 SYSTEM BLOCK")
        return

    kernel_report = run_kernel_check()
    if not kernel_report.get("ok"):
        print("🚫 KERNEL BLOCK")
        return

    message = generate_commit_message(diff)
    git_commit(message)


# -----------------------------
# DEBOUNCED TRIGGER
# -----------------------------
def trigger_commit():
    global timer

    if timer:
        timer.cancel()

    timer = threading.Timer(DEBOUNCE_SECONDS, safe_commit)
    timer.start()


# -----------------------------
# WATCHER
# -----------------------------
class ChangeHandler(FileSystemEventHandler):

    def on_modified(self, event):
        global last_event_time

        if not event.src_path.endswith(".py"):
            return

        now = time.time()
        if now - last_event_time < 2.0:
            return

        last_event_time = now

        print(f"🧠 Change detected: {event.src_path}")

        try:
            time.sleep(0.3)

            ast_check = run_ast_kernel_check(event.src_path)
            if not ast_check.get("ok", False):
                print("🚫 AST BLOCK")
                return

        except Exception as e:
            print("⚠️ AST ERROR (ignored):", e)
            return

        trigger_commit()


# -----------------------------
# START WATCHER
# -----------------------------
def start_auto_commit():
    observer = Observer()
    observer.schedule(ChangeHandler(), path=".", recursive=True)

    observer.start()
    print("🤖 Auto-commit running (STABLE MODE)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_auto_commit()