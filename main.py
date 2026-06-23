# main.py

from agent.router import route_request
from agent.tools.web_tools import http_get
from agent.registry import registry
from agent.config import load_config
from agent.kernel_loader import load_kernel

# -----------------------------
# TOOL REGISTRATION
# -----------------------------
registry.register("http_get", http_get)

# -----------------------------
# SYSTEM BOOT
# -----------------------------
kernel = load_kernel()
profile, mode = load_config()

print(f"🧠 Kernel loaded")
print(f"🧠 Agent starting in {mode.upper()} mode")
print("Type 'exit' to quit.\n")

# -----------------------------
# KERNEL PREVIEW (SAFE DEBUG)
# -----------------------------
try:
    print("---- KERNEL PREVIEW ----")
    print(kernel.get("raw", "")[:200])
    print("------------------------\n")
except Exception as e:
    print(f"⚠️ Kernel preview error: {e}")

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    user_input = input("APP IDEA > ")

    if user_input.lower().strip() == "exit":
        break

    response = route_request(
        user_input,
        profile=profile,
        tools=registry,
        kernel=kernel
    )

    print("\n--- RESPONSE ---")
    print(response)
    print("----------------\n")