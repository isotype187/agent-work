import requests
import time
DEBUG = False

# -----------------------------
# INSTANT RESPONSES (ULTRA LIGHT)
# -----------------------------
INSTANT_RULES = {
    "hello": "Hey 👋",
    "hi": "Hey 👋",
    "help": "Ask: 'generate app idea' or 'describe tool'",
    "ping": "pong ⚡",
    "status": "Agent running",
}


# -----------------------------
# INSTANT MODE CHECK
# -----------------------------
def is_simple(prompt: str) -> bool:
    if not prompt:
        return True

    p = prompt.strip().lower()

    if p in INSTANT_RULES:
        return True

    if len(p) <= 5:
        return True

    return False


def instant_response(prompt: str) -> str:
    return INSTANT_RULES.get(
        prompt.strip().lower(),
        "⚡ Instant response"
    )


# -----------------------------
# MAIN LLM CALL (PROFILE DRIVEN)
# -----------------------------
def ask_llm(prompt: str, profile: dict):
    """
    SINGLE LLM ENTRY POINT.
    Everything goes through here.
    """

    # -------------------------
    # INSTANT MODE (NO OLLAMA)
    # -------------------------
    if is_simple(prompt):
        
        if DEBUG:
            print("⚡ Instant mode")
        return instant_response(prompt)

    # -------------------------
    # PROFILE SETTINGS
    # -------------------------
    model = profile.get("model", "phi3")
    keep_alive = profile.get("keep_alive", "2m")

    try:
        start = time.time()

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "keep_alive": keep_alive
            },
            timeout=180
        )

        data = response.json()

        elapsed = time.time() - start
        
        if DEBUG:
            print(f"🧠 MODEL: {model}")
            print(f"⏱ TIME: {elapsed:.2f}s")

        return data.get("response", "[ERROR] No response")

    except Exception as e:
        return f"[LLM ERROR] {str(e)}"