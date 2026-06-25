import subprocess
from datetime import datetime


# -----------------------------
# SAFE RUNNER
# -----------------------------
def run(cmd):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=isinstance(cmd, str)
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"


# -----------------------------
# AUTO COMMIT MESSAGE GENERATOR
# -----------------------------
def build_commit_message(diff: str):
    diff = (diff or "").lower()

    tags = []

    if "fix" in diff:
        tags.append("fix")
    if "add" in diff:
        tags.append("add")
    if "remove" in diff:
        tags.append("remove")
    if "refactor" in diff:
        tags.append("refactor")

    tag_str = ", ".join(tags) if tags else "update"
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"{tag_str}: auto commit @ {time_str}"


# -----------------------------
# GET DIFF
# -----------------------------
def get_diff():
    return run(["git", "diff"])


# -----------------------------
# CORE PIPELINE
# -----------------------------
def git_push(prompt: str = ""):
    """
    One-word tool entry:
    push → add → commit → push
    """

    try:
        # 1. Stage everything
        run(["git", "add", "."])

        # 2. Get diff for message generation
        diff = get_diff()

        # 3. Build commit message
        message = build_commit_message(diff + " " + prompt)

        # 4. Commit
        commit_result = run(["git", "commit", "-m", message])

        # 5. Push
        push_result = run(["git", "push"])

        return {
            "status": "success",
            "commit_message": message,
            "commit_output": commit_result,
            "push_output": push_result
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"{type(e).__name__}: {e}"
        }