import os
import time

SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "venv",
}

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


def iter_python_files(path):
    if os.path.isfile(path):
        if path.endswith(".py"):
            yield path
        return

    if not os.path.isdir(path):
        return

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in files:
            if filename.endswith(".py"):
                yield os.path.join(root, filename)


def run_realtime_check(file_path):
    issues = []

    for python_file in iter_python_files(file_path):
        issues.extend(detect_structure_violations(python_file))

    return {
        "ok": len(issues) == 0,
        "issues": issues
    }
