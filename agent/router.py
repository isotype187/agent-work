import ast
from agent.llm import ask_llm, instant_response
from agent.config import load_config

DEBUG = False


# -----------------------------
# AST SELF AUDIT (SAFE DEBUG ONLY)
# -----------------------------
def self_audit_router():
    issues = []

    try:
        with open(__file__, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        functions = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        ]

        if len(functions) != len(set(functions)):
            issues.append("⚠️ Duplicate function definitions detected")

        if "route_request" not in functions:
            issues.append("⚠️ route_request missing")

    except Exception as e:
        issues.append(f"⚠️ Self-audit failed: {type(e).__name__}: {e}")

    return issues


# -----------------------------
# TOOL DETECTION (SINGLE SOURCE OF TRUTH)
# -----------------------------
def select_tool(prompt: str):
    p = prompt.lower().strip()

    # WEB TOOL
    if any(x in p for x in ["http", "https", "fetch", "scrape", "http_get"]):
        return "http_get"

    # GIT TOOL (single command abstraction)
    if any(x in p for x in ["push", "git push", "commit", "save project", "upload code"]):
        return "git_push"

    # STATUS TOOL
    if p in {"status", "git status"}:
        return "git_status"

    return None


# -----------------------------
# INTENT DETECTION (TRUTH = TOOL FIRST)
# -----------------------------
def detect_intent(prompt: str) -> str:
    p = prompt.lower().strip()

    # TOOL ALWAYS TAKES PRIORITY
    if select_tool(prompt):
        return "tool"

    if p in {"hi", "hello", "hey", "yo", "ping"}:
        return "instant"

    if len(p) <= 2:
        return "instant"

    return "llm"


# -----------------------------
# PAYLOAD EXTRACTION
# -----------------------------
def extract_payload(prompt: str):
    for token in prompt.split():
        if token.startswith("http"):
            return token
    return prompt


# -----------------------------
# TOOL EXECUTION WRAPPER
# -----------------------------
def run_tool(tools, tool_name, payload):
    if not tools:
        return "[TOOL: NO REGISTRY]"

    try:
        tool_fn = None

        if isinstance(tools, dict):
            tool_fn = tools.get(tool_name)
        else:
            tool_fn = getattr(tools, "get", lambda x: None)(tool_name)

        if not tool_fn:
            return f"[TOOL NOT FOUND: {tool_name}]"

        return tool_fn(payload)

    except Exception as e:
        return f"⚠️ TOOL ERROR: {type(e).__name__}: {e}"


# -----------------------------
# MAIN ROUTER
# -----------------------------
def route_request(
    prompt: str,
    tools=None,
    profile=None,
    memory=None,
    session_id: str = "default",
    kernel=None
):

    if profile is None:
        profile, _ = load_config()

    intent = detect_intent(prompt)

    # -----------------------------
    # DEBUG
    # -----------------------------
    if DEBUG:
        issues = self_audit_router()
        if issues:
            print("🧠 ROUTER ISSUES:")
            for i in issues:
                print(" -", i)

        print(f"🧭 intent={intent}")

    # -----------------------------
    # INSTANT MODE
    # -----------------------------
    if intent == "instant":
        return instant_response(prompt)

    # -----------------------------
    # TOOL MODE
    # -----------------------------
    if intent == "tool":
        tool_name = select_tool(prompt)
        payload = extract_payload(prompt)

        result = run_tool(tools, tool_name, payload)

        if memory:
            memory.add(session_id, "tool", str(result))

        return result

    # -----------------------------
    # LLM MODE
    # -----------------------------
    try:
        result = ask_llm(
            prompt=prompt,
            profile=profile,
            memory=memory,
            session_id=session_id
        )

        if memory:
            memory.add(session_id, "assistant", str(result))

        return result

    except Exception as e:
        return f"⚠️ LLM ERROR: {type(e).__name__}: {e}"