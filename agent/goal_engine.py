from agent.goal_graph import create_goal, get_ready_goals


def generate_goals(issues, state_history):
    text = " ".join(issues).lower()

    roots = []

    if "kernel" in text:
        roots.append("reduce_kernel_violations")

    if "ast" in text:
        roots.append("reduce_ast_errors")

    if "realtime" in text:
        roots.append("improve_realtime_consistency")

    if state_history.count("BLOCKED") > 2:
        roots.append("reduce_system_blocking")

    if not roots:
        roots.append("achieve_clean_commit_state")

    for r in roots:
        create_goal(r, priority=0.85)

    return roots


def get_current_goal():
    ready = get_ready_goals()

    if not ready:
        return None

    top = ready[0]

    return {
        "goal": top["goal"],
        "id": top["id"],
        "priority": top.get("priority", 0.5)
    }