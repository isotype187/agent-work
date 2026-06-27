from pathlib import Path


KERNEL_PATH = Path("agent_kernel.md")


def load_kernel():
    """
    Loads the agent kernel file and returns the runtime kernel structure.
    """
    if not KERNEL_PATH.exists():
        raise FileNotFoundError("agent_kernel.md not found")

    try:
        content = KERNEL_PATH.read_text(encoding="utf-8", errors="replace")

        return {
            "raw": content,
            "loaded": True,
            "path": str(KERNEL_PATH)
        }
    except Exception as e:
        return {
            "raw": "",
            "loaded": False,
            "path": str(KERNEL_PATH),
            "error": str(e)
        }


def get_kernel_raw(kernel):
    """
    Safe extractor for kernel raw content.
    """
    if isinstance(kernel, dict):
        return kernel.get("raw", "")

    if isinstance(kernel, str):
        return kernel

    return ""


def extract_section(kernel_text, section_name: str):
    """
    Simple markdown section extractor.
    """
    if isinstance(kernel_text, dict):
        kernel_text = kernel_text.get("raw", "")

    if not kernel_text:
        return None

    try:
        sections = kernel_text.split("##")
        for section in sections:
            if section_name.lower() in section.lower():
                return section.strip()
    except Exception:
        return None

    return None
