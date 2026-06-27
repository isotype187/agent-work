import os
from agent.executor import run

os.environ["PYTHONIOENCODING"] = "utf-8"


# -----------------------------
# SAFE EXECUTION (NO STREAM THREADS)
# -----------------------------
def safe_run(cmd):
    """
    Fully safe subprocess execution.
    NEVER triggers _readerthread crashes.
    """

    return run(cmd)
