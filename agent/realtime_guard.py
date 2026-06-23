import os
import time

BLOCKED_PATTERNS = [
    ("core.py", "router.py"),  # bad coupling
    ("tools/", "core"),        # inverted dependency
]


def scan_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().lower()
    except Exception:
        return ""


def detect_structure_violations(changed_file):
    issues = []

    content = scan_file(changed_file)

    # RULE 1 — no cross-layer contamination
    if "core.py" in changed_file:
        if "router" in content:
            issues.append("Core file referencing router directly")

    if "router.py" in changed_file:
        if "tool" in content and "decision" in content:
            issues.append("Router containing tool logic or decision logic")

    if "tools" in changed_file and "router" in content:
        issues.append("Tool layer referencing router (violation)")

    return issues


def run_realtime_check(file_path):
    return {
        "ok": True if not detect_structure_violations(file_path) else False,
        "issues": detect_structure_violations(file_path)
    }