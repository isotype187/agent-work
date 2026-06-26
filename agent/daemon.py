import threading
import time
import sys

from agent.runtime import safe_run


class AgentDaemon:
    def __init__(self, interval=5):
        self.interval = interval
        self.running = False
        self.thread = None

    def _cycle(self):
        while self.running:
            try:
                result = safe_run(
                    [sys.executable, "-c", "print('DAEMON CYCLE COMPLETE')"],
                    capture_output=True,
                    text=True,
                )

                print(result["stdout"].strip())
                print("DAEMON GOAL: achieve_clean_commit_state")

                safe_run(
                    [sys.executable, "-c", "print('reduce_kernel_violations')"],
                    capture_output=True,
                    text=True,
                )

            except Exception as e:
                print(f"DAEMON ERROR: {type(e).__name__}: {e}")

            time.sleep(self.interval)

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._cycle, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
