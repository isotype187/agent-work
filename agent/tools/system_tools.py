import subprocess
from registry import registry


def run_cmd(cmd):
    try:
        # Normalize input: ensure list unless explicitly string shell command
        if isinstance(cmd, str):
            process = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
        else:
            process = subprocess.run(
                cmd,
                shell=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

        return (process.stdout or "") + (process.stderr or "")

    except Exception as e:
        return f"RUN_CMD ERROR: {type(e).__name__}: {e}"


registry.register("run_cmd", run_cmd)