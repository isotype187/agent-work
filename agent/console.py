import sys


def configure_console_encoding():
    """
    Keep Windows redirected stdout/stderr from crashing on Unicode output.
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
