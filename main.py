# main.py

from agent.env_boot import load_project_root
load_project_root()

try:
    from agent.console import configure_console_encoding
    configure_console_encoding()
except Exception:
    pass

from agent.config import load_config
from agent.daemon import AgentDaemon
from agent.kernel_loader import load_kernel
from agent.memory import Memory
from agent.registry import registry
from agent.router import route_request
from agent.tools.git_snapshot import git_snapshot
from agent.tools.git_tool import git_push, git_status
from agent.tools.kernel_info_tool import kernel_info
from agent.tools.kernel_tool import kernel_update
from agent.tools.web_tools import http_get

try:
    from agent.system_integrity import run_system_check
    INTEGRITY_ENABLED = True
except Exception:
    INTEGRITY_ENABLED = False


registry.register("http_get", http_get)
registry.register("git_push", git_push)
registry.register("git_status", git_status)
registry.register("snapshot", git_snapshot)
registry.register("kernel_update", kernel_update)
registry.register("kernel_info", kernel_info)


kernel = load_kernel()
profile, mode = load_config()

print("Kernel loaded")
print(f"Agent starting in {mode.upper()} mode")
print("Type 'exit' to quit.\n")

memory = Memory()
session_id = "default"

try:
    print("---- KERNEL PREVIEW ----")
    raw = kernel.get("raw") if isinstance(kernel, dict) else str(kernel)
    print(raw[:200])
    print("------------------------\n")
except Exception as e:
    print(f"Kernel preview error: {e}")

if INTEGRITY_ENABLED:
    report = run_system_check(kernel)
    if report.get("issues"):
        print("SYSTEM INTEGRITY WARNINGS:")
        for issue in report["issues"]:
            print(" -", issue)
        print("")
    else:
        print("System integrity: OK\n")


daemon = AgentDaemon(interval=5)

try:
    daemon.start()
    print("Daemon mode: ACTIVE\n")
except Exception as e:
    print("Daemon failed:", e)


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

    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Runtime error:", e)


print("\nShutting down...")

try:
    daemon.stop()
except Exception:
    pass

print("Exit complete")
