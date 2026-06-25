# agent/system_integrity.py

import ast
from pathlib import Path


def run_system_check(kernel=None):
    """
    Structural integrity checker for the agent system.
    Detects missing files, router structure issues, and kernel inconsistencies.
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
    router_path = Path("agent/router.py")

    if router_path.exists():
        try:
            code = router_path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(code)

            functions = [
                node.name
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            ]

            # Must contain main entry point
            if "route_request" not in functions:
                report["issues"].append("❌ router missing route_request")

            # Detect duplicates (should never happen, but good safeguard)
            if functions.count("route_request") > 1:
                report["issues"].append("⚠️ duplicate route_request detected")

        except SyntaxError as e:
            report["issues"].append(f"❌ router syntax error: {e}")

        except Exception as e:
            report["issues"].append(f"⚠️ router parse failed: {type(e).__name__}: {e}")

    # -----------------------------
    # KERNEL VALIDATION (STABILIZED)
    # -----------------------------
    if kernel is None:
        report["issues"].append("⚠️ kernel not loaded into integrity layer")

    else:
        # Accept multiple kernel formats safely (prevents false failures)
        if isinstance(kernel, dict):
            pass  # expected format

        elif isinstance(kernel, str):
            # allowed but flagged as informational
            report["issues"].append("⚠️ kernel is raw string (expected dict after parsing)")

        else:
            report["issues"].append(
                f"⚠️ kernel unexpected type: {type(kernel).__name__}"
            )

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