import json
import os
import time


LEARNING_PATH = "memory/kernel_learning.json"


def load_learning():
    try:
        with open(LEARNING_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_learning(data):
    os.makedirs(os.path.dirname(LEARNING_PATH), exist_ok=True)

    with open(LEARNING_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def record_issue(issue):
    data = load_learning()

    entry = data.get(issue, {
        "count": 0,
        "last_seen": None
    })

    entry["count"] += 1
    entry["last_seen"] = time.time()

    data[issue] = entry

    save_learning(data)


def analyze_issues(issues):
    data = load_learning()

    insights = []

    for issue in issues:
        record_issue(issue)

        stats = data.get(issue, {})

        if stats.get("count", 0) >= 3:
            insights.append({
                "issue": issue,
                "pattern": "recurring_violation",
                "count": stats["count"],
                "suggestion": "This is a repeated architecture failure. Consider refactoring root module rather than patching symptoms."
            })

    return insights


def run_learning_cycle(issues):
    return {
        "insights": analyze_issues(issues)
    }