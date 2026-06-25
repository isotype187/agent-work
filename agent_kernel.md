# 🧠 Agent Kernel File v1.2

---

## Generated

Last update:
2026-06-24 21:35

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

## Current Project Files

- main.py
- memory.py
- __init__.py
- agent\ast_kernel_guard.py
- agent\autonomous_loop.py
- agent\auto_commit.py
- agent\config.py
- agent\context_builder.py
- agent\daemon.py
- agent\env_boot.py
- agent\execution_planner.py
- agent\executor.py
- agent\goal_engine.py
- agent\goal_graph.py
- agent\hardware.py
- agent\kernel.py
- agent\kernel_guard.py
- agent\kernel_loader.py
- agent\learning_kernel.py
- agent\llm.py
- agent\memory.py
- agent\pipeline_controller.py
- agent\pipeline_memory.py
- agent\pipeline_state.py
- agent\prompt.py
- agent\realtime_guard.py
- agent\recursive_planner.py
- agent\reflection_engine.py
- agent\registry.py
- agent\router.py
- agent\runtime.py
- agent\self_audit.py
- agent\self_healer.py
- agent\self_modulator.py
- agent\snapshot_builder.py
- agent\state_controller.py
- agent\system_integrity.py
- agent\watchdog_runner.py
- agent\__init__.py
- agent\tools\decorator.py
- agent\tools\file_tools.py
- agent\tools\git_snapshot.py
- agent\tools\git_tool.py
- agent\tools\kernel_info_tool.py
- agent\tools\kernel_tool.py
- agent\tools\system_tools.py
- agent\tools\web_tools.py
- agent\tools\__init__.py

---

## Tool Philosophy

Tools execute.
Router decides.
LLM reasons.
Memory stores state.

---

## Available Command Layer

push
→ git commit and push

snapshot
→ project checkpoint

kernel
→ regenerate kernel file

kernel info
→ copy kernel contents

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

