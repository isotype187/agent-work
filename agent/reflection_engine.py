import time
from collections import defaultdict

from agent.goal_graph import create_goal, get_graph


STATE_HISTORY_FILE = "memory/state_history.json"


def _load_history():
    try:
        import json
        with open(STATE_HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_history(history):
    import json
    import os

    os.makedirs("memory", exist_ok=True)

    with open(STATE_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-200:], f, indent=2)


def record_cycle(state):
    history = _load_history()

    history.append({
        "time": time.time(),
        "state": state
    })

    _save_history(history)


def analyze_patterns(history):
    """
    Detect repeated system behaviors.
    """
    pattern_count = defaultdict(int)

    for entry in history[-50:]:
        state = entry.get("state", "unknown")
        pattern_count[state] += 1

    return pattern_count


def generate_reflection_goals():
    history = _load_history()
    graph = get_graph()

    if len(history) < 5:
        return []

    patterns = analyze_patterns(history)

    new_goals = []

    # -----------------------------
    # REPETITION DETECTION
    # -----------------------------
    if patterns.get("BLOCKED", 0) > 3:
        new_goals.append("reduce_system_blocking_loops")

    if patterns.get("COMMIT_FAIL", 0) > 2:
        new_goals.append("improve_commit_stability")

    if patterns.get("IDLE", 0) > 10:
        new_goals.append("increase_goal_activation_density")

    if patterns.get("VALIDATING", 0) > 8:
        new_goals.append("optimize_validation_overhead")

    # -----------------------------
    # STRUCTURAL OBSERVATION
    # -----------------------------
    if len(graph) > 50:
        new_goals.append("reduce_goal_graph_bloat")

    # -----------------------------
    # CREATE META-GOALS
    # -----------------------------
    for g in new_goals:
        create_goal(g, priority=0.7)

    return new_goals