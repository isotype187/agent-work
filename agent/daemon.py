import time
import threading

from agent.goal_graph import (
    stabilize_graph,
    get_ready_goals
)

from agent.pipeline_controller import run_full_pipeline


class AgentDaemon:

    def __init__(self, interval=10):
        self.interval = interval
        self.running = False
        self.thread = None

    def _tick(self):
        while self.running:
            try:
                # 🧠 keep system stable
                stabilize_graph()

                ready = get_ready_goals()

                if ready:
                    goal = ready[0]

                    print(f"🧠 DAEMON GOAL: {goal['goal']}")

                    report = run_full_pipeline(
                        file_path=".",
                        diff=""
                    )

                    if report.get("ok"):
                        print("✅ DAEMON CYCLE COMPLETE")
                    else:
                        print("🚫 DAEMON BLOCKED")

                else:
                    print("🟡 DAEMON IDLE: no goals")

            except Exception as e:
                print("🔥 DAEMON ERROR:", e)

            time.sleep(self.interval)

    def start(self):
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._tick,
            daemon=True
        )

        self.thread.start()
        print("🚀 DAEMON MODE STARTED")

    def stop(self):
        self.running = False

        if self.thread:
            self.thread.join()