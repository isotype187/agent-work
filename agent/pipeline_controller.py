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

from agent.execution_planner import build_execution_plan
from agent.goal_engine import generate_goals


def run_full_pipeline(file_path, diff):
    enter("VALIDATING")

    issues = []
    state_history = []

    plan = build_execution_plan(
        issues,
        state_history
    )

    checks = plan.get(
        "checks",
        [
            "system",
            "kernel",
            "ast",
            "realtime"
        ]
    )

    if "system" in checks:
        result = run_system_check()

        if result.get("issues"):
            issues.extend(result["issues"])

    if "kernel" in checks:
        result = run_kernel_check()

        if not result.get("ok"):
            issues.extend(
                result.get("issues", [])
            )

    if "realtime" in checks:
        result = run_realtime_check(file_path)

        if not result.get("ok"):
            issues.extend(
                result.get("issues", [])
            )

    if "ast" in checks:
        result = run_ast_kernel_check(file_path)

        if not result.get("ok"):
            issues.extend(
                result.get("issues", [])
            )

    audit = run_self_audit(
        core_decision="pipeline_execution",
        router_output="git_commit",
        issues=issues
    )

    if not audit.get("ok"):
        enter("BLOCKED")
        state_history.append("BLOCKED")

        healing = run_self_healer(issues)

        enter("HEALING")
        state_history.append("HEALING")

        learning = run_learning_cycle(issues)

        memory = run_pipeline_memory(
            issues,
            healing
        )

        config = apply_feedback(
            issues,
            state_history
        )

        goals = generate_goals(
            issues,
            state_history
        )

        return {
            "ok": False,
            "state": current(),
            "plan": plan,
            "issues": issues,
            "healing": healing,
            "learning": learning,
            "memory": memory,
            "config": config,
            "goals": goals
        }

    enter("COMMIT")
    state_history.append("COMMIT")

    learning = run_learning_cycle(issues)

    memory = run_pipeline_memory(
        issues,
        None
    )

    config = apply_feedback(
        issues,
        state_history
    )

    goals = generate_goals(
        issues,
        state_history
    )

    enter("CLEAN")

    return {
        "ok": True,
        "state": current(),
        "plan": plan,
        "issues": [],
        "healing": None,
        "learning": learning,
        "memory": memory,
        "config": config,
        "goals": goals
    }