import json
import time
import os


CONFIG_PATH = "memory/self_mod_config.json"


DEFAULT_CONFIG = {
    "ast_weight": 1.0,
    "kernel_weight": 1.0,
    "realtime_weight": 1.0,
    "audit_weight": 1.0,
    "retry_limit": 10,
    "strict_mode": True
}


def _load():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG.copy()


def _save(cfg):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def get_config():
    return _load()


def apply_feedback(issues, state_history):
    """
    Adjust system behavior based on observed patterns.
    This is NOT code rewriting — it's parameter tuning.
    """

    cfg = _load()

    issue_count = len(issues)

    # -----------------------------
    # RULE 1: Increase strictness if unstable
    # -----------------------------
    if issue_count > 5:
        cfg["strict_mode"] = True
        cfg["ast_weight"] = min(cfg["ast_weight"] + 0.1, 2.0)
        cfg["kernel_weight"] = min(cfg["kernel_weight"] + 0.1, 2.0)

    # -----------------------------
    # RULE 2: Relax if overly blocked
    # -----------------------------
    if state_history.count("BLOCKED") > 3:
        cfg["strict_mode"] = False
        cfg["realtime_weight"] = max(cfg["realtime_weight"] - 0.1, 0.5)

    # -----------------------------
    # RULE 3: Stabilize retry behavior
    # -----------------------------
    if state_history.count("HEALING") > 3:
        cfg["retry_limit"] = max(cfg["retry_limit"] - 1, 3)

    # -----------------------------
    # RULE 4: Escalation safety clamp
    # -----------------------------
    if issue_count == 0:
        cfg["retry_limit"] = min(cfg["retry_limit"] + 1, 15)

    cfg["last_update"] = time.time()

    _save(cfg)

    return cfg