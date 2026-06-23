import os
import json
import time


MEMORY_PATH = "memory/pipeline_evolution.json"


def _load():
    try:
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "violations": {},
            "suggestions": {}
        }


def _save(data):
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)

    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def record_violation(issue):
    data = _load()

    if issue not in data["violations"]:
        data["violations"][issue] = {
            "count": 0,
            "last_seen": None
        }

    data["violations"][issue]["count"] += 1
    data["violations"][issue]["last_seen"] = time.time()

    _save(data)


def record_suggestion(issue, suggestion):
    data = _load()

    if issue not in data["suggestions"]:
        data["suggestions"][issue] = []

    data["suggestions"][issue].append({
        "text": suggestion,
        "time": time.time()
    })

    _save(data)


def analyze_pipeline_evolution(issues, healing):
    data = _load()

    adjustments = []

    for issue in issues:
        record_violation(issue)

        stats = data["violations"].get(issue, {})

        if stats.get("count", 0) >= 3:
            adjustments.append({
                "issue": issue,
                "type": "pipeline_hotspot",
                "recommendation": (
                    "Repeated failure detected. "
                    "Consider moving this check earlier in pipeline "
                    "or strengthening pre-commit validation."
                )
            })

    if healing:
        for repair in healing.get("repairs", []):
            record_suggestion(
                repair.get("issue", "unknown"),
                repair.get("suggested_fix", "")
            )

    return {
        "adjustments": adjustments
    }


def run_pipeline_memory(issues, healing):
    return analyze_pipeline_evolution(issues, healing)