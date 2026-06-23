# agent/router.py

from agent.llm import ask_llm, instant_response
from agent.config import load_config

DEBUG = False


# -----------------------------
# ROUTER SELF-AUDIT SYSTEM
# -----------------------------

def self_audit_router():
    """
    Lightweight structural integrity check.
    Runs on every request (debug only).
    """

    issues = []

    try:
        with open(__file__, "r", encoding="utf-8") as f:
            code = f.read()

        # Detect duplicated LLM blocks
        llm_block_marker = "LLM MODE (MAIN PATH)"
        if code.count(llm_block_marker) > 1:
            issues.append("⚠️ Duplicate LLM block detected")

        # Detect duplicated return patterns (basic safeguard)
        if code.count("return llm(prompt, profile)") > 1:
            issues.append("⚠️ Duplicate LLM return path detected")

        # Detect accidental repeated function definitions
        if code.count("def route_request") > 1:
            issues.append("⚠️ Duplicate route_request definition detected")

    except Exception as e:
        issues.append(f"⚠️ Self-audit failed: {str(e)}")

    return issues


# -----------------------------
# INTENT DETECTION
# -----------------------------

def detect_intent(prompt: str) -> str:
    p = prompt.lower().strip()

    if p in {"hi", "hello", "hey", "yo"}:
        return "instant"

    if any(x in p for x in ["status", "memory", "uptime", "running"]):
        return "instant"

    if any(x in p for x in ["http", "https", "fetch", "scrape"]):
        return "tool"

    return "llm"


# -----------------------------
# MAIN ROUTER
# -----------------------------

def route_request(prompt: str, tools=None, profile=None, llm=None, kernel=None):
    """
    Single brain entry point for entire agent system
    """

    if profile is None:
        profile, _ = load_config()

    intent = detect_intent(prompt)

    # -----------------------------
    # SELF AUDIT (DEBUG MODE ONLY)
    # -----------------------------
    if DEBUG:
        issues = self_audit_router()
        if issues:
            print("🧠 ROUTER SELF-AUDIT REPORT:")
            for i in issues:
                print(" -", i)

        print(f"🧭 ROUTER → {intent} | MODEL → {profile['model']}")

    # -------------------------
    # INSTANT MODE
    # -------------------------
    if intent == "instant":
        return instant_response(prompt)

    # -------------------------
    # TOOL MODE
    # -------------------------
    if intent == "tool":
        selected_tool = None

        p = prompt.lower()

        if any(x in p for x in ["http", "https", "fetch", "scrape"]):
            selected_tool = "http_get"

        if selected_tool and tools:
            try:
                if isinstance(tools, dict):
                    tool_fn = tools.get(selected_tool)
                elif hasattr(tools, "get"):
                    tool_fn = tools.get(selected_tool)
                else:
                    tool_fn = None

                if tool_fn:
                    return tool_fn(prompt)

            except Exception as e:
                return f"⚠️ Tool error: {str(e)}"

        return "[TOOL SYSTEM READY - NOT YET WIRED]"

    # -------------------------
    # LLM MODE
    # -------------------------
    if llm is None:
        llm = ask_llm

    try:
        return llm(prompt, profile)
    except Exception as e:
        return f"⚠️ LLM error: {str(e)}"