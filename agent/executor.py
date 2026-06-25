import subprocess

def run(cmd):
    """
    Single unified subprocess executor.
    Replaces ALL subprocess usage across project.
    """

    try:
        # Normalize command behavior
        shell_mode = isinstance(cmd, str)

        result = subprocess.run(
            cmd,
            shell=shell_mode,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        return {
            "code": result.returncode,
            "stdout": result.stdout or "",
            "stderr": result.stderr or ""
        }

    except Exception as e:
        return {
            "code": -1,
            "stdout": "",
            "stderr": f"EXECUTOR ERROR: {type(e).__name__}: {e}"
        }