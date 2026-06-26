import subprocess


DEFAULT_ENCODING = "utf-8"
DEFAULT_ERRORS = "replace"


def safe_run(args, **kwargs):
    """
    Run a subprocess with stable text decoding across Windows shells.
    """
    if kwargs.get("text") or kwargs.get("capture_output"):
        kwargs.setdefault("encoding", DEFAULT_ENCODING)
        kwargs.setdefault("errors", DEFAULT_ERRORS)

    result = subprocess.run(args, **kwargs)

    return {
        "returncode": result.returncode,
        "stdout": result.stdout or "",
        "stderr": result.stderr or "",
        "raw": result,
    }
