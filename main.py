from agent.router import route_request
from agent.tools.web_tools import http_get
from agent.registry import registry
from agent.config import load_config
from agent.kernel_loader import load_kernel
from agent.daemon import daemon
from agent.env_boot import load_project_root

load_project_root()
try:
    from agent.system_integrity import run_system_check
    INTEGRITY_ENABLED = True
except Exception:
    INTEGRITY_ENABLED = False


registry.register("http_get", http_get)

kernel = load_kernel()
profile, mode = load_config()

print("🧠 Kernel loaded")
print(f"🧠 Agent starting in {mode.upper()} mode")
print("Type 'exit' to quit.\n")

try:
    print("---- KERNEL PREVIEW ----")
    raw = kernel.get("raw", "")
    print(raw[:200] if isinstance(raw, str) else str(raw)[:200])
    print("------------------------\n")
except Exception as e:
    print(f"⚠️ Kernel preview error: {e}")

if INTEGRITY_ENABLED:
    report = run_system_check(kernel)

    if report.get("issues"):
        print("🧠 SYSTEM INTEGRITY WARNINGS:")
        for issue in report["issues"]:
            print(" -", issue)
        print("")
    else:
        print("🧠 System integrity: OK\n")


# -----------------------------
# START DAEMON (AUTONOMOUS LAYER)
# -----------------------------
try:
    daemon.start()
    print("🚀 Daemon mode: ACTIVE\n")
except Exception as e:
    print("⚠️ Daemon failed to start:", e)


# -----------------------------
# MAIN LOOP (INTERACTIVE LAYER)
# -----------------------------
while True:
    try:
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

    except KeyboardInterrupt:
        break

    except Exception as e:
        print("🔥 Runtime error:", e)


# -----------------------------
# SHUTDOWN CLEANLY
# -----------------------------
print("\n🛑 Shutting down...")

try:
    daemon.stop()
except Exception:
    pass

print("✅ Exit complete")