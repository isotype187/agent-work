# agent/tools/kernel_tool.py

from pathlib import Path
from datetime import datetime
from agent.executor import run as executor_run

KERNEL_PATH = Path("agent_kernel.md")


# -----------------------------
# SAFE COMMAND RUNNER
# -----------------------------
def run(cmd):
    result = executor_run(cmd)
    return (result.get("stdout") or "") + (result.get("stderr") or "")


# -----------------------------
# FILE CLASSIFICATION
# -----------------------------
def classify(file_path: str):
    p = file_path.lower()

    if any(x in p for x in ["watchdog", "auto_commit", "daemon", "runtime", "log"]):
        return "system"

    if any(x in p for x in ["guard", "cache", "temp"]):
        return "ignore"

    return "core"


# -----------------------------
# PROJECT SCAN (SINGLE SOURCE OF TRUTH)
# -----------------------------
def scan_project():
    core, system = [], []

    for path in Path(".").rglob("*.py"):
        if "venv" in str(path):
            continue

        f = str(path)
        category = classify(f)

        if category == "ignore":
            continue

        if category == "system":
            system.append(f)
        else:
            core.append(f)

    return core, system


# -----------------------------
# BUILD KERNEL
# -----------------------------
def build_kernel():
    core, system = scan_project()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""# Agent Kernel

---

## Generated

Last update: {now}

---

## Project Identity

Modular Python AI Agent system.

---

## Current Architecture

main.py
→ startup
→ registry wiring
→ input loop

agent/

router.py
→ intent detection
→ tool routing

llm.py
→ model communication
→ memory injection

registry.py
→ central tool registry

memory.py
→ persistent sessions

kernel_loader.py
→ kernel loading

tools/

---

## Core Files
{chr(10).join("- " + x for x in core)}

---

## System Modules
{chr(10).join("- " + x for x in system)}

---

## Tool Philosophy

Tools execute.
Router decides.
LLM reasons.
Memory stores state.

---

## Available Command Layer

push → git commit and push  
snapshot → project checkpoint  
kernel → regenerate kernel file  
kernel info → copy kernel contents  

---

## Kernel Rules

Kernel defines:
- architecture
- boundaries
- system behavior

Memory defines:
- runtime knowledge
- learned state

---

## Development Rules

- Full file replacements preferred
- Keep modules separated
- Avoid duplicate logic
- Use registry for tools

---
"""


# -----------------------------
# WRITE KERNEL
# -----------------------------
def update_kernel():
    content = build_kernel()
    KERNEL_PATH.write_text(content, encoding="utf-8")
    return content


# -----------------------------
# COMMAND ENTRY
# -----------------------------
def kernel_update(prompt=""):
    try:
        update_kernel()

        run(["git", "add", "agent_kernel.md"])

        commit = run([
            "git",
            "commit",
            "-m",
            "kernel: automated architecture update"
        ])

        push = run(["git", "push"])

        return {
            "status": "success",
            "message": "🧠 Kernel fully regenerated",
            "commit": commit,
            "push": push
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"{type(e).__name__}: {e}"
        }
