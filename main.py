from agent.router import route_request
from agent.tools.web_tools import http_get
from agent.registry import registry
from agent.config import load_config

# Register tools once (ensures they are globally available)
registry.register("http_get", http_get)

# Load the config to decide if we’re on laptop or desktop
profile, mode = load_config()

print(f"🧠 Agent starting in {mode.upper()} mode")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("APP IDEA > ")

    if user_input.lower().strip() == "exit":
        break

    response = route_request(
        user_input,
        profile=profile,  # Pass the mode-specific profile
        tools=registry   # Tools registry for routing
    )

    print("\n--- RESPONSE ---")
    print(response)
    print("----------------\n")