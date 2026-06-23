import time

from agent.pipeline_controller import run_full_pipeline
from agent.pipeline_state import get_state
from agent.goal_engine import evaluate_goal


MAX_CYCLES = 12
SLEEP_INTERVAL = 1.5


def run_autonomous_loop(file_path, diff):

    cycle = 0

    while cycle < MAX_CYCLES:

        cycle += 1

        print(f"\n🧠 CYCLE {cycle}")
        print(f"STATE: {get_state()}")

        report = run_full_pipeline(file_path=file_path, diff=diff)

        state = report.get("state")
        issues = report.get("issues", [])

        goal = evaluate_goal(state, issues)

        print(f"🎯 GOAL STATUS: {goal['reason']} | progress={goal['progress']}")

        # -----------------------------
        # STOP CONDITIONS (GOAL DRIVEN)
        # -----------------------------
        if goal["achieved"]:
            print("🟢 GOAL ACHIEVED — SYSTEM STABLE")
            return report

        if cycle >= MAX_CYCLES:
            print("⚠️ MAX CYCLES REACHED — SAFETY STOP")
            return {
                "ok": False,
                "state": state,
                "error": "goal_not_reached"
            }

        if state == "BLOCKED":
            print("🚫 BLOCKED → retrying healing loop")

        if state == "HEALING":
            print("🛠 HEALING ACTIVE")

        time.sleep(SLEEP_INTERVAL)