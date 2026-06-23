# 🧠 Agent Kernel File v1.1

---

## Project Identity

Modular Python-based AI Agent system called "agent-work"

GitHub Repo:
https://github.com/isotype187/agent-work

---

## 🏗️ Core Architecture

main.py → entry point only (startup + input loop)

agent/
  core.py → reasoning engine (decides what to do)
  router.py → selects tool/module

tools/
  web_utils.py → HTTP/web operations
  system_utils.py → OS/subprocess operations

memory/
  memory.py → memory interface logic
  memory.json → persistent structured memory

config.json → global configuration

---

## 🧠 Design Principles

- Strict separation of concerns
- No “god files”
- Core does NOT execute tools
- Tools do NOT make decisions
- Router is the only dispatcher
- Keep modules small and replaceable

---

## 🔁 Execution Flow

Input → Core → Router → Tool → Response → Memory Update

---

## ⚙️ Execution Enforcement Rules

- Core MUST call router for every request
- Router MUST return a single tool or response
- Tools MUST NOT call other tools directly
- Memory updates ONLY happen after response generation
- Any violation = execution rejection or fallback path

---

## 🧠 Memory System (Tiered)

### 🟢 Working Memory
- Temporary session state
- Not persisted long-term

### 🟡 Long-Term Memory (memory.json)
Stores ONLY:
- stable facts
- preferences
- system configuration
- learned behaviors

### 🔵 Summary Memory
Compressed historical knowledge:
- replaces raw logs
- stores condensed insights
- prevents memory bloat

Example:
{
  "summary_2026_06_23": "Refactored agent into modular architecture with core/router/tool separation"
}

---

## 🧠 Memory Rules

- Never store raw conversations
- Always classify memory writes:
  - fact
  - preference
  - system_state
  - summary
  - temporary

- Periodically compress old memory into summaries

---

## 🔌 Tool System

- Tools are isolated functions
- Stateless when possible
- Registered through a central system
- NEVER called directly by core
- All tool access must go through router

---

## 🔄 Kernel Loading Contract

When starting any chat or session:

- Kernel must be provided in full
- Kernel defines system behavior for session
- If kernel is missing → system runs in degraded mode
- No assumptions allowed outside kernel scope

---

## 🔁 Kernel vs Memory Separation

Kernel = system design + rules + architecture  
Memory = runtime knowledge + learned state  

Kernel is static unless explicitly changed  
Memory evolves during execution

---

## ⚙️ Git Status

Repository initialized and synced:

Branch: main  
Remote: origin  
URL: https://github.com/isotype187/agent-work

---

## 🚀 Development Rules

- Prefer full-file replacements (drop-ins only)
- Partial snippets only when explicitly requested
- Do not merge unrelated responsibilities into one file
- Maintain strict modular boundaries
- Keep main.py minimal
- Treat architecture as stable contract unless explicitly refactoring

---

## 🧠 System Goal

Build a scalable agent system that behaves like:

- ChatGPT-style reasoning layer (core)
- Command router (decision layer)
- Tool execution system (action layer)
- Structured memory system (state layer)

---

## 🧩 Current Status

- Git initialized ✔
- GitHub connected ✔
- Core architecture defined ✔
- Memory system designed ✔
- Implementation phase in progress ⏳

---

## ⚡ Purpose of This File

This is the single source of truth for:

- architecture rules
- system behavior
- memory design
- execution flow
- development constraints
- system boundaries