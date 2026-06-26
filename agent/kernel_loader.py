from pathlib import Path

KERNEL_PATH = Path("agent_kernel.md")


def load_kernel():
    """
    Loads the agent kernel file and returns the runtime kernel structure.
    This acts as the system-level configuration for the agent.
    """
    if not KERNEL_PATH.exists():
        raise FileNotFoundError("agent_kernel.md not found. Kernel is required to start agent.")

    with open(KERNEL_PATH, "r", encoding="utf-8") as f:
        kernel_content = f.read()

    return {
        "raw": kernel_content,
        "path": str(KERNEL_PATH),
    }


def extract_section(kernel_text: str, section_name: str):
    """
    Optional helper for later:
    lets us pull structured parts of the kernel if needed.
    """
    if isinstance(kernel_text, dict):
        kernel_text = kernel_text.get("raw", "")

    sections = kernel_text.split("##")
    for section in sections:
        if section_name.lower() in section.lower():
            return section.strip()

    return None
