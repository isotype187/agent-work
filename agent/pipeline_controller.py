# agent/pipeline_controller.py

from agent.system_integrity import run_system_check
from agent.kernel_guard import run_kernel_check
from agent.realtime_guard import run_realtime_check
from agent.ast_kernel_guard import run_ast_kernel_check
from agent.self_audit import run_self_audit
from agent.self_healer import run_self_healer
from agent.learning_kernel import run_learning_cycle
from agent.pipeline_memory import run_pipeline_memory
from agent.self_modulator import apply_feedback

from agent.state_controller import enter, current


def run_full_pipeline(file_path, diff):

    enter("VALIDATING")

    issues = []
    state_history = []

    # -----------------------------
    # SYSTEM GATES
    # -----------------------------
    system = run_system_check()
    if system.get("issues"):
        issues.extend(system["issues"])

    kernel = run_kernel_check()
    if not kernel.get("ok"):
        issues.extend(kernel.get("issues", []))

    runtime = run_realtime_check(file_path)
    if not runtime.get("ok"):
        issues.extend(runtime.get("issues", []))

    ast = run_ast_kernel_check(file_path)
    if not ast.get("ok"):
        issues.extend(ast.get("issues", []))

    # -----------------------------
    # SELF AUDIT (ENFORCED GATE)
    # -----------------------------
    audit = run_self_audit(
        core_decision="pipeline_execution",
        router_output="git_commit",
        issues=issues
    )

    if not audit.get("ok"):
        issues.extend(audit.get("issues", []))
        enter("BLOCKED")
        state_history.append("BLOCKED")

        # -----------------------------
        # HEALING PHASE
        # -----------------------------
        healing = run_self_healer(issues)
        enter("HEALING")
        state_history.append("HEALING")

        learning = run_learning_cycle(issues)
        memory = run_pipeline_memory(issues, healing)

        # -----------------------------
        # SELF MODULATION (ADAPTIVE TUNING)
        # -----------------------------
        config = apply_feedback(issues, state_history)

        return {
            "ok": False,
            "state": current(),
            "issues": issues,
            "healing": healing,
            "learning": learning,
            "pipeline_memory": memory,
            "config": config
        }

    # -----------------------------
    # SUCCESS PATH
    # -----------------------------
    enter("COMMIT")
    state_history.append("COMMIT")

    learning = run_learning_cycle(issues)
    memory = run_pipeline_memory(issues, None)

    # -----------------------------
    # SELF MODULATION (SUCCESS FEEDBACK)
    # -----------------------------
    config = apply_feedback(issues, state_history)

    enter("CLEAN")

    return {
        "ok": True,
        "state": current(),
        "issues": [],
        "healing": None,
        "learning": learning,
        "pipeline_memory": memory,
        "config": config
    }