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

def route_request(prompt: str, tools=None, profile=None, llm=None, kernel=None):
    """
    Single brain entry point for entire agent system
    """

    if profile is None:
        profile, _ = load_config()

    intent = detect_intent(prompt)

    # -----------------------------
    # 🧠 KERNEL LOAD (SAFE LAYER)
    # -----------------------------
    rules = {}
    tool_policy = "open"

    if isinstance(kernel, dict):
        rules = kernel.get("rules", {}) or {}
        tool_policy = rules.get("rules", {}).get("tool_access", "open")

    def is_tool_allowed(tool_name: str) -> bool:
        if tool_policy == "strict":
            try:
                if isinstance(tools, dict):
                    return tool_name in tools
                if hasattr(tools, "registry"):
                    return tool_name in tools.registry
                return True
            except Exception:
                return True
        return True

    if DEBUG:
        print(f"🧭 ROUTER → {intent} | MODEL → {profile['model']} | TOOL_POLICY → {tool_policy}")

    # -------------------------
    # INSTANT MODE (NO LLM)
    # -------------------------
    if intent == "instant":
        return instant_response(prompt)

    # -------------------------
    # TOOL MODE
    # -------------------------
    if intent == "tool":
        # basic heuristic tool selection (your system can evolve later)
        selected_tool = None

        p = prompt.lower()

        if any(x in p for x in ["http", "https", "fetch", "scrape"]):
            selected_tool = "http_get"

        # 🧠 KERNEL ENFORCEMENT
        if selected_tool and not is_tool_allowed(selected_tool):
            return "🚫 Tool blocked by kernel policy (strict mode)"

        # TOOL EXECUTION
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
    # LLM MODE (MAIN PATH)
    # -------------------------
    if llm is None:
        llm = ask_llm

    try:
        return llm(prompt, profile)
    except Exception as e:
        return f"⚠️ LLM error: {str(e)}"