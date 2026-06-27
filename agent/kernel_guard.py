# agent/kernel_guard.py

from agent.executor import run


KERNEL_PATH = "agent_kernel.md"


def load_kernel():
    try:
        with open(KERNEL_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def get_git_diff():
    result = run(["git", "diff"])
    return result.get("stdout", "")


def kernel_violation_check(diff: str, kernel: str):
    issues = []

    diff_lower = diff.lower()
    kernel_lower = kernel.lower()

    if "core.py" in diff_lower and "router.py" in diff_lower:
        issues.append("Core and Router changes detected together (violates separation of concerns)")

    if "tools/" not in kernel_lower:
        issues.append("Kernel missing tools definition block")

    if "router" in diff_lower and "tool" in diff_lower and "core" in diff_lower:
        issues.append("Cross-layer modification detected (core/router/tool overlap)")

    return issues


def run_kernel_check():
    kernel = load_kernel()
    diff = get_git_diff()
    issues = kernel_violation_check(diff, kernel)

    return {
        "ok": len(issues) == 0,
        "issues": issues
    }
