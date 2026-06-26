# main.py

from agent.console import configure_console_encoding
from agent.router import route_request
from agent.tools.web_tools import http_get
from agent.registry import registry
from agent.config import load_config
from agent.kernel_loader import load_kernel

configure_console_encoding()

# OPTIONAL: system integrity layer (safe import)
try:
    from agent.system_integrity import run_system_check
    INTEGRITY_ENABLED = True
except Exception:
    INTEGRITY_ENABLED = False

# -----------------------------
# TOOL REGISTRATION
# -----------------------------
registry.register("http_get", http_get)

# -----------------------------
# BOOT SYSTEM
# -----------------------------
kernel = load_kernel()
profile, mode = load_config()

print(f"🧠 Kernel loaded")
print(f"🧠 Agent starting in {mode.upper()} mode")
print("Type 'exit' to quit.\n")

# -----------------------------
# KERNEL PREVIEW (SAFE)
# -----------------------------
try:
    print("---- KERNEL PREVIEW ----")
    raw = kernel.get("raw", "")
    print(raw[:200] if isinstance(raw, str) else str(raw)[:200])
    print("------------------------\n")
except Exception as e:
    print(f"⚠️ Kernel preview error: {e}")

# -----------------------------
# SYSTEM INTEGRITY CHECK (BOOT)
# -----------------------------
if INTEGRITY_ENABLED:
    report = run_system_check(kernel)  # Pass the kernel explicitly

    if report["issues"]:
        print("🧠 SYSTEM INTEGRITY WARNINGS:")
        for issue in report["issues"]:
            print(" -", issue)
        print("")
    else:
        print("🧠 System integrity: OK\n")

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
        kernel=kernel  # Pass kernel here as well for routing
    )

    print("\n--- RESPONSE ---")
    print(response)
    print("----------------\n")
