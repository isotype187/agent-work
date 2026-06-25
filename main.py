# main.py

from agent.env_boot import load_project_root
load_project_root()

from agent.router import route_request
from agent.tools.web_tools import http_get
from agent.tools.git_tool import git_push
from agent.registry import registry
from agent.config import load_config
from agent.kernel_loader import load_kernel
from agent.daemon import AgentDaemon
from agent.memory import Memory
from agent.tools.git_snapshot import git_snapshot

try:
    from agent.system_integrity import run_system_check
    INTEGRITY_ENABLED = True
except Exception:
    INTEGRITY_ENABLED = False


# -----------------------------
# TOOL REGISTRATION
# -----------------------------
registry.register("http_get", http_get)
registry.register("git_push", git_push)
registry.register("snapshot", git_snapshot)


# -----------------------------
# BOOT SYSTEM
# -----------------------------
kernel = load_kernel()
profile, mode = load_config()

print("🧠 Kernel loaded")
print(f"🧠 Agent starting in {mode.upper()} mode")
print("Type 'exit' to quit.\n")


# -----------------------------
# MEMORY + SESSION
# -----------------------------
memory = Memory()
session_id = "default"


# -----------------------------
# KERNEL PREVIEW
# -----------------------------
try:
    print("---- KERNEL PREVIEW ----")
    raw = kernel.get("raw") if isinstance(kernel, dict) else str(kernel)
    print(raw[:200])
    print("------------------------\n")
except Exception as e:
    print(f"⚠️ Kernel preview error: {e}")


# -----------------------------
# SYSTEM INTEGRITY
# -----------------------------
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
# DAEMON
# -----------------------------
daemon = AgentDaemon(interval=5)

try:
    daemon.start()
    print("🚀 Daemon mode: ACTIVE\n")
except Exception as e:
    print("⚠️ Daemon failed:", e)


# -----------------------------
# MAIN LOOP (CLEAN PIPELINE ONLY)
# -----------------------------
while True:
    try:
        user_input = input("APP IDEA > ").strip()

        if user_input.lower() == "exit":
            break

        response = route_request(
            prompt=user_input,
            profile=profile,
            tools=registry,
            kernel=kernel,
            memory=memory,
            session_id=session_id
        )

        print("\n--- RESPONSE ---")
        print(response)
        print("----------------\n")

    except Exception as e:
        print("🔥 Runtime error:", e)


# -----------------------------
# SHUTDOWN
# -----------------------------
print("\n🛑 Shutting down...")

try:
    daemon.stop()
except Exception:
    pass

print("✅ Exit complete")