def build_context(prompt: str, kernel, memory, profile: dict):
    parts = []

    # Kernel (system identity)
    if kernel:
        parts.append("=== KERNEL ===")
        parts.append(str(kernel)[:2000])

    # Memory (conversation history)
    if memory:
        try:
            parts.append("=== MEMORY (RECENT CHAT) ===")
            for m in memory.recent(6):
                parts.append(f"User: {m['user']}")
                parts.append(f"Assistant: {m['assistant']}")
        except Exception:
            pass

    # Profile
    parts.append("=== PROFILE ===")
    parts.append(str(profile))

    # Current input
    parts.append("=== USER ===")
    parts.append(prompt)

    return "\n".join(parts)