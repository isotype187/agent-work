# agent/llm.py

import requests
import time

DEBUG = False


# -----------------------------
# INSTANT RESPONSES
# -----------------------------
INSTANT_RULES = {
    "hello": "Hey 👋",
    "hi": "Hey 👋",
    "help": "Ask: 'generate app idea' or 'describe tool'",
    "ping": "pong ⚡",
    "status": "Agent running",
}


def is_simple(prompt: str) -> bool:
    if not prompt:
        return True

    p = prompt.strip().lower()

    return p in INSTANT_RULES or len(p) <= 5


def instant_response(prompt: str) -> str:
    return INSTANT_RULES.get(prompt.strip().lower(), "⚡ Instant response")


# -----------------------------
# MEMORY BUILDER
# -----------------------------
def build_prompt(prompt: str, memory_context: str | None):
    if not memory_context:
        return prompt

    return f"""[MEMORY CONTEXT]
{memory_context}

[USER INPUT]
{prompt}
"""


# -----------------------------
# MAIN LLM ENTRY
# -----------------------------
def ask_llm(prompt: str, profile: dict, memory=None, session_id="default"):
    try:
        # instant bypass
        if is_simple(prompt):
            resp = instant_response(prompt)

            if memory:
                memory.add(session_id, "assistant", resp)

            return resp

        model = profile.get("model", "phi3")
        keep_alive = profile.get("keep_alive", "2m")

        # -------------------------
        # MEMORY READ
        # -------------------------
        memory_context = None
        if memory:
            try:
                memory_context = memory.get(session_id)
                memory.add(session_id, "user", prompt)
            except Exception:
                memory_context = None

        final_prompt = build_prompt(prompt, memory_context)

        # -------------------------
        # OLLAMA CALL
        # -------------------------
        start = time.time()

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": final_prompt,
                "stream": False,
                "keep_alive": keep_alive
            },
            timeout=180
        )

        data = response.json()
        output = data.get("response", "[ERROR] No response")

        if DEBUG:
            print(f"🧠 MODEL: {model}")
            print(f"⏱ TIME: {time.time() - start:.2f}s")

        if memory:
            memory.add(session_id, "assistant", output)

        return output

    except Exception as e:
        return f"[LLM ERROR] {type(e).__name__}: {e}"