import time


def run_self_audit(core_decision, router_output, issues):
    """
    Enforced architectural audit gate.

    This does NOT just report issues.
    It can HARD-BLOCK pipeline progression.
    """

    audit_issues = []
    blocked = False

    # -----------------------------
    # RULE 1: Core must never execute actions directly
    # -----------------------------
    forbidden_core_actions = {
        "git_commit",
        "execute",
        "run_tool",
        "subprocess",
        "system_call"
    }

    if core_decision in forbidden_core_actions:
        audit_issues.append(
            f"BLOCK: Core attempted direct execution -> {core_decision}"
        )
        blocked = True

    # -----------------------------
    # RULE 2: Router must produce valid terminal action
    # -----------------------------
    valid_router_outputs = {
        "git_commit",
        "noop",
        "defer"
    }

    if router_output not in valid_router_outputs:
        audit_issues.append(
            f"BLOCK: Invalid router output -> {router_output}"
        )
        blocked = True

    # -----------------------------
    # RULE 3: System overload protection
    # -----------------------------
    if len(issues) > 8:
        audit_issues.append(
            "BLOCK: Excessive system violations detected (possible architecture drift)"
        )
        blocked = True

    # -----------------------------
    # RULE 4: Cascading failure detection
    # -----------------------------
    if len(issues) > 0 and core_decision == "unsafe_execute":
        audit_issues.append(
            "BLOCK: Unsafe execution attempt during active violation state"
        )
        blocked = True

    # -----------------------------
    # RESULT
    # -----------------------------
    return {
        "ok": not blocked,
        "blocked": blocked,
        "issues": audit_issues,
        "timestamp": time.time()
    }