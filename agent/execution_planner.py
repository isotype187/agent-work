from agent.goal_engine import get_current_goal


def build_execution_plan(issues, state_history):
    goal_data = get_current_goal()

    if not goal_data:
        return {
            "goal": "achieve_clean_commit_state",
            "checks": [
                "system",
                "kernel",
                "ast",
                "realtime"
            ],
            "strict": True
        }

    goal = goal_data.get("goal")

    if goal == "reduce_kernel_violations":
        return {
            "goal": goal,
            "checks": [
                "kernel",
                "ast"
            ],
            "strict": True
        }

    if goal == "reduce_ast_errors":
        return {
            "goal": goal,
            "checks": [
                "ast"
            ],
            "strict": True
        }

    if goal == "improve_realtime_consistency":
        return {
            "goal": goal,
            "checks": [
                "realtime"
            ],
            "strict": False
        }

    if goal == "reduce_system_blocking":
        return {
            "goal": goal,
            "checks": [
                "system",
                "kernel"
            ],
            "strict": False
        }

    if goal == "reduce_healing_frequency":
        return {
            "goal": goal,
            "checks": [
                "system",
                "kernel",
                "ast"
            ],
            "strict": False
        }

    return {
        "goal": goal,
        "checks": [
            "system",
            "kernel",
            "ast",
            "realtime"
        ],
        "strict": True
    }