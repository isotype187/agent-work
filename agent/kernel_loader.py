from pathlib import Path

KERNEL_PATH = Path("agent_kernel.md")


def load_kernel():
    """
    Loads kernel file and returns structured dict.
    """

    if not KERNEL_PATH.exists():
        raise FileNotFoundError("agent_kernel.md not found")

    try:
        with open(KERNEL_PATH, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        return {
            "raw": content,
            "loaded": True,
            "path": str(KERNEL_PATH)
        }

    except Exception as e:
        return {
            "raw": "",
            "loaded": False,
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


def extract_section(kernel_text: str, section_name: str):
    """
    Simple markdown section extractor.
    """

    if not kernel_text:
        return None

    try:
        sections = kernel_text.split("##")

        for s in sections:
            if section_name.lower() in s.lower():
                return s.strip()

        return None

    except Exception:
        return None