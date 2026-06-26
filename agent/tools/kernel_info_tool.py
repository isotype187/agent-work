import pyperclip
from pathlib import Path


KERNEL_PATH = Path("agent_kernel.md")


# -----------------------------
# KERNEL INFO TOOL
# -----------------------------
def kernel_info(prompt: str = ""):
    """
    Copies current kernel contents to clipboard.
    """

    try:
        if not KERNEL_PATH.exists():
            return {
                "status": "error",
                "message": "agent_kernel.md not found"
            }

        content = KERNEL_PATH.read_text(
            encoding="utf-8"
        )

        pyperclip.copy(content)

        return {
            "status": "success",
            "message": "🧠 Kernel copied to clipboard",
            "size": len(content)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"{type(e).__name__}: {e}"
        }