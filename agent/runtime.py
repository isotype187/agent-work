import subprocess
import os

os.environ["PYTHONIOENCODING"] = "utf-8"


# -----------------------------
# SAFE EXECUTION (NO STREAM THREADS)
# -----------------------------
def safe_run(cmd):
    """
    Fully safe subprocess execution.
    NEVER triggers _readerthread crashes.
    """

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=0
        )

        # CRITICAL: communicate() avoids streaming thread entirely
        out, err = proc.communicate()

        return {
            "code": proc.returncode,
            "stdout": out,
            "stderr": err
        }

    except Exception as e:
        return {
            "code": -1,
            "stdout": "",
            "stderr": f"RUNTIME ERROR: {type(e).__name__}: {e}"
        }