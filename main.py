from agent.router import route_request
from agent.tools.web_tools import http_get
from agent.registry import registry
from agent.config import load_config
from agent.kernel_loader import load_kernel


def boot_agent():
    # Load kernel (system rules / architecture spec)
    kernel = load_kernel()

    print("🧠 Kernel loaded successfully")
    print("---- KERNEL ACTIVE (preview) ----")
    print(kernel[:250])
    print("----------------------------------\n")

    return kernel


def setup_agent():
    # Register tools once
    registry.register("http_get", http_get)

    # Load config (profile + mode)
    profile, mode = load_config()

    print(f"🧠 Agent starting in {mode.upper()} mode")
    print("Type 'exit' to quit.\n")

    return profile, mode


def main():
    # Boot phase (system initialization)
    kernel = boot_agent()
    profile, mode = setup_agent()

    # Runtime loop
    while True:
        user_input = input("APP IDEA > ")

        if user_input.lower().strip() == "exit":
            print("👋 Shutting down agent...")
            break

        response = route_request(
            user_input,
            profile=profile,
            tools=registry
        )

        print("\n--- RESPONSE ---")
        print(response)
        print("----------------\n")


if __name__ == "__main__":
    main()