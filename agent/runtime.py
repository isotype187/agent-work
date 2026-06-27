import os

from agent.executor import run


os.environ["PYTHONIOENCODING"] = "utf-8"


def safe_run(cmd, **kwargs):
    """
    Compatibility wrapper around the unified executor.
    Extra subprocess-style kwargs are accepted for older call sites.
    """
    return run(cmd)
