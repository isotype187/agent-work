# agent/tools/web_tools.py
import requests

def http_get(url: str):
    try:
        r = requests.get(url, timeout=10)
        return {
            "status": r.status_code,
            "text": r.text[:500]  # keep it small for now
        }
    except Exception as e:
        return {"error": str(e)}