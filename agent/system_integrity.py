# agent/system_integrity.py

import ast
from pathlib import Path


# -----------------------------
# CORE INTEGRITY CHECKER
# -----------------------------

def run_system_check(kernel=None):
    """
    Checks structural consistency across the agent system.
    """

    report = {
        "issues": [],
        "files_checked": []
    }

    project_files = [
        "agent/router.py",
        "main.py",
        "agent/registry.py",
        "agent/kernel_loader.py",
    ]

    # -----------------------------
    # FILE EXISTENCE CHECK
    # -----------------------------
    for file in project_files:
        path = Path(file)

        if not path.exists():
            report["issues"].append(f"❌ Missing file: {file}")
        else:
            report["files_checked"].append(file)

    # -----------------------------
    # ROUTER STRUCTURE CHECK
    # -----------------------------
    try:
        router_path = Path("agent/router.py")

        if router_path.exists():
            code = router_path.read_text(encoding="utf-8")
            tree = ast.parse(code)

            functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]

            if "route_request" not in functions:
                report["issues"].append("❌ router missing route_request")

            if functions.count("route_request") > 1:
                report["issues"].append("⚠️ duplicate route_request detected")

    except Exception as e:
        report["issues"].append(f"⚠️ router parse failed: {e}")

    # -----------------------------
    # KERNEL VALIDATION
    # -----------------------------
    if kernel is None:
        report["issues"].append("⚠️ kernel not loaded into integrity layer")
    else:
        if not isinstance(kernel, dict):
            report["issues"].append("⚠️ kernel is not a dict structure")

    # -----------------------------
    # RESULT
    # -----------------------------
    return report


# -----------------------------
# OPTIONAL DEBUG RUN
# -----------------------------
if __name__ == "__main__":
    result = run_system_check()

    print("\n🧠 SYSTEM INTEGRITY REPORT\n")

    print("Files checked:")
    for f in result["files_checked"]:
        print(" -", f)

    print("\nIssues:")
    if not result["issues"]:
        print("✔ No issues detected")
    else:
        for i in result["issues"]:
            print(" -", i)