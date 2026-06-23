import time

from agent.pipeline_controller import run_full_pipeline
from agent.pipeline_state import get_state


MAX_CYCLES = 10
SLEEP_INTERVAL = 1.5


def run_autonomous_loop(file_path, diff):

    cycle = 0

    while cycle < MAX_CYCLES:

        cycle += 1

        print(f"\n🧠 AUTONOMOUS CYCLE {cycle}")
        print(f"STATE: {get_state()}")

        report = run_full_pipeline(file_path=file_path, diff=diff)

        state = report.get("state")

        # -----------------------------
        # TERMINATION CONDITIONS
        # -----------------------------
        if report["ok"]:
            print("🟢 SYSTEM STABILIZED (COMMIT OK)")
            return report

        if state == "CLEAN":
            print("🟡 CLEAN STATE REACHED EARLY EXIT")
            return report

        if state == "BLOCKED":
            print("🚫 BLOCKED → entering healing cooldown")

        if state == "HEALING":
            print("🛠 HEALING ACTIVE")

        if state == "RETRY":
            print("🔁 RETRYING PIPELINE")

        time.sleep(SLEEP_INTERVAL)

    print("⚠️ MAX CYCLES REACHED — SAFETY STOP")
    return {
        "ok": False,
        "state": get_state(),
        "error": "max_cycles_reached"
    }