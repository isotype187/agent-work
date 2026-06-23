# agent/router.py

from agent.llm import ask_llm, instant_response
from agent.config import load_config
DEBUG = False

# -----------------------------
# ROUTING CORE
# -----------------------------

def detect_intent(prompt: str) -> str:
    """
    Ultra-light intent detection (NO LLM, NO HEAVY OPS)
    """

    p = prompt.lower().strip()

    # instant chat responses
    if p in {"hi", "hello", "hey", "yo"}:
        return "instant"

    # system queries
    if any(x in p for x in ["status", "memory", "uptime", "running"]):
        return "instant"

    # tool hinting (future expansion)
    if any(x in p for x in ["http", "https", "fetch", "scrape"]):
        return "tool"

    # default → LLM
    return "llm"


# -----------------------------
# MAIN ROUTER
# -----------------------------

def route_request(prompt: str, tools=None, profile=None, llm=None):
    """
    Single brain entry point for entire agent system
    """

    if profile is None:
        profile, _ = load_config()

    intent = detect_intent(prompt)

    
    if DEBUG:
        print(f"🧭 ROUTER → {intent} | MODEL → {profile['model']}")

    # -------------------------
    # INSTANT MODE (NO LLM)
    # -------------------------
    if intent == "instant":
        return instant_response(prompt)

    # -------------------------
    # TOOL MODE (PLACEHOLDER FOR NOW)
    # -------------------------
    if intent == "tool":
        return "[TOOL SYSTEM READY - NOT YET WIRED]"

    # -------------------------
    # LLM MODE (MAIN PATH)
    # -------------------------
    if llm is None:
        llm = ask_llm  # fallback safety

    return llm(prompt, profile)