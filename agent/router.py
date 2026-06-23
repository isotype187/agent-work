# agent/router.py

import ast
from agent.llm import ask_llm, instant_response
from agent.config import load_config

DEBUG = False


# -----------------------------
# AST-BASED SELF AUDIT (HARDENED)
# -----------------------------

def self_audit_router():
    """
    Structural integrity check using AST (real syntax parsing).
    Safe, fast, and accurate.
    """

    issues = []

    try:
        with open(__file__, "r", encoding="utf-8") as f:
            source = f.read()

        # -----------------------------
        # PARSE INTO AST
        # -----------------------------
        tree = ast.parse(source)

        # Track functions
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

        # Detect duplicate function definitions
        if len(functions) != len(set(functions)):
            issues.append("⚠️ Duplicate function definitions detected (AST)")

        # Ensure route_request exists exactly once
        if functions.count("route_request") > 1:
            issues.append("⚠️ Multiple route_request definitions detected")

        # Basic structural sanity check: must contain router
        if "route_request" not in functions:
            issues.append("⚠️ route_request missing from router file")

        # Detect syntax health implicitly (AST parse failure would already throw)

    except SyntaxError as e:
        issues.append(f"🚨 SYNTAX ERROR in router.py: {e}")

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
    # HARDENED SELF AUDIT (DEBUG ONLY)
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