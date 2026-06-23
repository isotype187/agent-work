\# 🧠 Agent Kernel File v1



\## Project Identity

Modular Python-based AI Agent system called "agent-work".



GitHub Repo:

https://github.com/isotype187/agent-work



\---



\## 🏗️ Core Architecture



main.py → entry point only (startup + input loop)



agent/

&#x20; core.py → reasoning engine (decides what to do)

&#x20; router.py → selects tool/module



tools/

&#x20; web\_utils.py → HTTP/web operations

&#x20; system\_utils.py → OS/subprocess operations



memory/

&#x20; memory.py → memory interface logic

&#x20; memory.json → persistent structured memory



config.json → global configuration



\---



\## 🧠 Design Principles



\- Strict separation of concerns

\- No “god files”

\- Core does NOT execute tools

\- Tools do NOT make decisions

\- Router is the only dispatcher

\- Keep modules small and replaceable



\---



\## 🔁 Execution Flow



Input → Core → Router → Tool → Response → Memory Update



\---



\## 🧠 Memory System (Tiered)



\### 🟢 Working Memory

Temporary session state

Not persisted long-term



\---



\### 🟡 Long-Term Memory (memory.json)

Stores ONLY:

\- stable facts

\- preferences

\- system configuration

\- learned behaviors



\---



\### 🔵 Summary Memory

Compressed historical knowledge:

\- replaces raw logs

\- stores condensed insights

\- prevents memory bloat



Example:

{

&#x20; "summary\_2026\_06\_23": "Refactored agent into modular architecture with core/router/tool separation"

}



\---



\## 🧠 Memory Rules



\- Never store raw conversations

\- Always classify memory writes:

&#x20; - fact

&#x20; - preference

&#x20; - system\_state

&#x20; - summary

&#x20; - temporary



\- Periodically compress old memory into summaries



\---



\## 🔌 Tool System



\- Tools are isolated functions

\- Stateless when possible

\- Registered through a central system

\- NEVER called directly by core



All tool access must go through router.



\---



\## ⚙️ Git Status



Repository is already initialized and pushed:



Branch: main  

Remote: origin  

URL: https://github.com/isotype187/agent-work



\---



\## 🚀 Development Rules



\- Prefer full-file replacements over snippets

\- Do not merge unrelated responsibilities into one file

\- Maintain strict modular boundaries

\- Keep main.py minimal

\- Treat architecture as stable contract unless explicitly refactoring



\---



\## 🧠 System Goal



Build a scalable agent system that behaves like:



\- ChatGPT-style reasoning layer (core)

\- Command router (decision layer)

\- Tool execution system (action layer)

\- Structured memory system (state layer)



\---



\## 🧩 Current Status



\- Git initialized ✔

\- GitHub connected ✔

\- Core architecture defined ✔

\- Memory system designed ✔

\- Implementation phase in progress ⏳



\---



\## ⚡ Purpose of This File



This is the single source of truth for:

\- architecture rules

\- system behavior

\- memory design

\- execution flow

\- development constraints



Use this file to restore context in any new chat.

