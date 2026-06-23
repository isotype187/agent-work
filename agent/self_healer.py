# agent/self_healer.py

import json
import os
import time


HEAL_LOG = "memory/self_heal_log.json"


def load_history():
    try:
        with open(HEAL_LOG, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return []


def save_history(history):
    os.makedirs(
        os.path.dirname(HEAL_LOG),
        exist_ok=True
    )

    with open(HEAL_LOG, "w", encoding="utf-8") as f:
        json.dump(
            history,
            f,
            indent=2
        )


def generate_fix(issue):
    issue_lower = issue.lower()

    if "core layer" in issue_lower:
        return (
            "Move tool selection logic into router.py. "
            "Core should only make decisions."
        )

    if "router" in issue_lower:
        return (
            "Remove direct execution logic. "
            "Route actions through registered tools."
        )

    if "tool" in issue_lower:
        return (
            "Keep tool modules isolated. "
            "Remove references to core decision logic."
        )

    if "kernel" in issue_lower:
        return (
            "Update architecture contract or modify code "
            "to match kernel rules."
        )

    return (
        "Review this change against agent_kernel.md "
        "and restore module boundaries."
    )


def analyze_failure(issues):

    repairs = []

    for issue in issues:
        repairs.append({
            "issue": issue,
            "suggested_fix": generate_fix(issue)
        })

    return repairs


def run_self_healer(issues):

    repairs = analyze_failure(issues)

    history = load_history()

    history.append({
        "timestamp": time.time(),
        "issues": issues,
        "repairs": repairs
    })

    save_history(history)

    return {
        "healing_available": len(repairs) > 0,
        "repairs": repairs
    }