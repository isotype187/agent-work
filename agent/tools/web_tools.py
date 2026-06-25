# agent/tools/web_tools.py
import requests
from agent.tools import tool

DEBUG = False


# -----------------------------
# CORE HTTP GET TOOL
# -----------------------------
@tool("http_get")
def http_get(url: str):
    """
    Basic HTTP GET tool.
    Safe, plugin-registered, registry-compatible.
    """

    try:
        if DEBUG:
            print(f"🌐 GET: {url}")

        r = requests.get(url, timeout=10)

        return {
            "ok": True,
            "status": r.status_code,
            "text": r.text[:1000],  # prevent memory explosion
            "headers": dict(r.headers)
        }

    except Exception as e:
        return {
            "ok": False,
            "error": f"{type(e).__name__}: {e}"
        }


# -----------------------------
# JSON FETCH TOOL (API FRIENDLY)
# -----------------------------
@tool("fetch_json")
def fetch_json(url: str):
    """
    Fetch JSON APIs cleanly.
    """

    try:
        if DEBUG:
            print(f"🌐 JSON GET: {url}")

        r = requests.get(url, timeout=10)
        r.raise_for_status()

        return {
            "ok": True,
            "data": r.json()
        }

    except Exception as e:
        return {
            "ok": False,
            "error": f"{type(e).__name__}: {e}"
        }


# -----------------------------
# SIMPLE PAGE PEEK TOOL
# -----------------------------
@tool("peek_page")
def peek_page(url: str):
    """
    Lightweight page preview (no parsing, just raw snippet).
    """

    try:
        r = requests.get(url, timeout=10)

        return {
            "ok": True,
            "snippet": r.text[:500]
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }