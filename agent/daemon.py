# agent/daemon.py

import threading
import time
from agent.runtime import safe_run


class AgentDaemon:
    def __init__(self, interval=5):
        self.interval = interval
        self.running = False
        self.thread = None

    def _cycle(self):
        while self.running:
            try:
                # Example safe heartbeat task
                # Replace ANY subprocess logic with safe_run()
                result = safe_run(["echo", "DAEMON CYCLE COMPLETE"])

                print(result["stdout"].strip())
                print("🧠 DAEMON GOAL: achieve_clean_commit_state")

                # Simulated cleanup task
                safe_run(["echo", "reduce_kernel_violations"])

            except Exception as e:
                print(f"⚠️ DAEMON ERROR: {type(e).__name__}: {e}")

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