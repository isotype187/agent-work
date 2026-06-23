# agent/pipeline_controller.py

from agent.system_integrity import run_system_check
from agent.kernel_guard import run_kernel_check
from agent.realtime_guard import run_realtime_check
from agent.ast_kernel_guard import run_ast_kernel_check
from agent.self_audit import run_self_audit
from agent.self_healer import run_self_healer
from agent.learning_kernel import run_learning_cycle
from agent.pipeline_memory import run_pipeline_memory

from agent.state_controller import enter, current


def run_full_pipeline(file_path, diff):

    enter("VALIDATING")

    issues = []

    system = run_system_check()
    if system["issues"]:
        issues.extend(system["issues"])

    kernel = run_kernel_check()
    if not kernel["ok"]:
        issues.extend(kernel["issues"])

    runtime = run_realtime_check(file_path)
    if not runtime["ok"]:
        issues.extend(runtime["issues"])

    ast = run_ast_kernel_check(file_path)
    if not ast["ok"]:
        issues.extend(ast["issues"])

    audit = run_self_audit(
        core_decision="pipeline_execution",
        router_output="git_commit",
        issues=issues
    )

    if not audit["ok"]:
        issues.extend(audit["issues"])

        enter("BLOCKED")

        healing = run_self_healer(issues)

        enter("HEALING")

        learning = run_learning_cycle(issues)

        memory = run_pipeline_memory(issues, healing)

        return {
            "ok": False,
            "state": current(),
            "issues": issues,
            "healing": healing,
            "learning": learning,
            "pipeline_memory": memory
        }

    enter("COMMIT")

    learning = run_learning_cycle(issues)

    memory = run_pipeline_memory(issues, None)

    enter("CLEAN")

    return {
        "ok": True,
        "state": current(),
        "issues": [],
        "healing": None,
        "learning": learning,
        "pipeline_memory": memory
    }