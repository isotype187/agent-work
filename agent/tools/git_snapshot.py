from datetime import datetime
from agent.executor import run as executor_run


# -----------------------------
# SAFE RUNNER
# -----------------------------
def run(cmd):
    result = executor_run(cmd)
    return (result.get("stdout") or "") + (result.get("stderr") or "")


# -----------------------------
# DIFF FOR MESSAGE BUILDING
# -----------------------------
def get_diff():
    return run(["git", "diff"])


# -----------------------------
# SMART SNAPSHOT MESSAGE
# -----------------------------
def build_message(diff: str, label: str):
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

    if label:
        return f"[{label}] {tag_str}: snapshot @ {time_str}"

    return f"{tag_str}: snapshot @ {time_str}"


# -----------------------------
# FULL SNAPSHOT PIPELINE
# -----------------------------
def git_snapshot(prompt: str = ""):
    """
    ONE COMMAND:
    snapshot → add → commit → push
    """

    try:
        # optional label support
        label = prompt.strip() if prompt else ""

        # 1. Stage everything
        run(["git", "add", "."])

        # 2. Get diff
        diff = get_diff()

        # 3. Build commit message
        message = build_message(diff, label)

        # 4. Commit
        commit_out = run(["git", "commit", "-m", message])

        # 5. Push
        push_out = run(["git", "push"])

        # 6. Optional status feedback
        status = run(["git", "status"])

        return {
            "status": "snapshot complete",
            "message": message,
            "commit_output": commit_out,
            "push_output": push_out,
            "git_status": status
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"{type(e).__name__}: {e}"
        }
