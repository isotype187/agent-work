from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from threading import Timer

from agent.snapshot_builder import build_snapshot

DEBOUNCE_TIME = 2.0  # seconds
timer = None


# -----------------------------
# DEBOUNCED HANDLER
# -----------------------------
def trigger_snapshot(kernel=None):
    global timer

    if timer:
        timer.cancel()

    timer = Timer(DEBOUNCE_TIME, lambda: build_snapshot(kernel))
    timer.start()


class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"🧠 Change detected: {event.src_path}")
            trigger_snapshot()


def start_watching():
    event_handler = ChangeHandler()
    observer = Observer()

    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    print("👀 Smart snapshot watcher running...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_watching()
