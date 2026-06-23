import time
import threading

from agent.reflection_engine import record_cycle, generate_reflection_goals
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
                stabilize_graph()

                # 🪞 REFLECTION STEP (NEW)
                generate_reflection_goals()

                ready = get_ready_goals()

                if ready:
                    goal = ready[0]

                    record_cycle(goal["goal"])

                    print(f"🧠 DAEMON GOAL: {goal['goal']}")

                    report = run_full_pipeline(
                        file_path=".",
                        diff=""
                    )

                    if report.get("ok"):
                        record_cycle("COMMIT_SUCCESS")
                        print("✅ DAEMON CYCLE COMPLETE")
                    else:
                        record_cycle("BLOCKED")
                        print("🚫 DAEMON BLOCKED")

                else:
                    record_cycle("IDLE")
                    print("🟡 DAEMON IDLE: no goals")

            except Exception as e:
                record_cycle("ERROR")
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