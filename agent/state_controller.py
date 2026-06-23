from agent.pipeline_state import get_state, set_state


VALID_STATES = {
    "CLEAN",
    "VALIDATING",
    "BLOCKED",
    "HEALING",
    "RETRY",
    "COMMIT"
}


TRANSITIONS = {
    "CLEAN": ["VALIDATING"],
    "VALIDATING": ["BLOCKED", "COMMIT"],
    "BLOCKED": ["HEALING"],
    "HEALING": ["RETRY"],
    "RETRY": ["VALIDATING"],
    "COMMIT": ["CLEAN"]
}


def enter(state):
    if state not in VALID_STATES:
        raise ValueError(f"Invalid state: {state}")

    set_state(state)


def current():
    return get_state()


def is_state(state):
    return get_state() == state


def allow_transition(from_state, to_state):
    return to_state in TRANSITIONS.get(from_state, [])


def transition(to_state):
    current_state = get_state()

    if to_state not in VALID_STATES:
        raise ValueError(f"Invalid state: {to_state}")

    if not allow_transition(current_state, to_state):
        raise RuntimeError(
            f"Illegal transition: {current_state} → {to_state}"
        )

    set_state(to_state)
    return get_state()