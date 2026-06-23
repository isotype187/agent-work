from agent.goal_graph import get_graph, get_ready_goals


MAX_DEPTH = 3


def build_plan(goal_id, graph, depth=0):
    if depth > MAX_DEPTH:
        return None

    node = graph.get(goal_id)

    if not node:
        return None

    plan = {
        "goal": node["goal"],
        "id": goal_id,
        "priority": node.get("priority", 0.5),
        "children": []
    }

    for child_id in node.get("children", []):
        child_plan = build_plan(child_id, graph, depth + 1)

        if child_plan:
            plan["children"].append(child_plan)

    return plan


def flatten_plan(plan, depth=0):
    if not plan:
        return []

    result = [{
        "goal": plan["goal"],
        "id": plan["id"],
        "priority": plan["priority"],
        "depth": depth
    }]

    for child in plan.get("children", []):
        result.extend(flatten_plan(child, depth + 1))

    return result


def evaluate_plan_score(flat_plan):
    score = 0

    for node in flat_plan:
        weight = 1 / (node["depth"] + 1)
        score += node["priority"] * weight

    return score


def generate_recursive_plans():
    graph = get_graph()
    ready = get_ready_goals()

    plans = []

    for root in ready:
        tree = build_plan(root["id"], graph)

        flat = flatten_plan(tree)

        score = evaluate_plan_score(flat)

        plans.append({
            "root": root["goal"],
            "root_id": root["id"],
            "score": score,
            "plan": flat
        })

    plans.sort(key=lambda x: x["score"], reverse=True)

    return plans


def get_best_plan():
    plans = generate_recursive_plans()

    if not plans:
        return None

    return plans[0]