import json
from agent.hardware import detect_mode

CONFIG_FILE = "config.json"


def load_config():
    """
    Single source of truth for system configuration.
    """

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    mode = cfg.get("mode", "auto")

    # -----------------------------
    # AUTO MODE RESOLUTION
    # -----------------------------
    if mode == "auto":
        mode = detect_mode()

    profiles = cfg.get("profiles", {})

    if mode not in profiles:
        raise ValueError(f"Invalid mode resolved: {mode}")

    return profiles[mode], mode