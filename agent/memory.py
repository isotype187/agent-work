# agent/memory.py

import json
import time
from pathlib import Path

MEMORY_FILE = Path("agent_memory.json")


class Memory:
    """
    Multi-session + compressed + semantic memory system.
    """

    def __init__(self):
        self.data = self._load()

    # =========================================================
    # LOAD / SAVE
    # =========================================================
    def _load(self):
        if not MEMORY_FILE.exists():
            return {"sessions": {}}

        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {"sessions": {}}

    def _save(self):
        MEMORY_FILE.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    # =========================================================
    # SESSION CORE
    # =========================================================
    def _ensure(self, session_id):
        if session_id not in self.data["sessions"]:
            self.data["sessions"][session_id] = {
                "created": time.time(),
                "messages": [],
                "summary": "",
                "keywords": {}
            }

    def get(self, session_id: str):
        """Router-compatible accessor"""
        self._ensure(session_id)
        return self.data["sessions"][session_id]

    # =========================================================
    # WRITE
    # =========================================================
    def add(self, session_id: str, role: str, content: str):
        self._ensure(session_id)

        session = self.data["sessions"][session_id]

        session["messages"].append({
            "role": role,
            "content": content,
            "ts": time.time()
        })

        # auto keyword indexing (lightweight semantic layer)
        for word in content.lower().split():
            if len(word) > 3:
                session["keywords"][word] = session["keywords"].get(word, 0) + 1

        self._maybe_compress(session_id)
        self._save()

    # =========================================================
    # READ
    # =========================================================
    def get_recent(self, session_id, limit=12):
        self._ensure(session_id)
        return self.data["sessions"][session_id]["messages"][-limit:]

    def get_full_context(self, session_id, limit=20):
        msgs = self.get_recent(session_id, limit)

        text = "\n".join(
            f"{m['role'].upper()}: {m['content']}"
            for m in msgs
        )

        summary = self.data["sessions"][session_id].get("summary", "")

        if summary:
            return f"[SUMMARY]\n{summary}\n\n[RECENT]\n{text}"

        return text

    # =========================================================
    # MULTI-CHAT SUPPORT
    # =========================================================
    def list_sessions(self):
        return list(self.data["sessions"].keys())

    def new_session(self, session_id: str):
        self._ensure(session_id)
        self._save()

    def switch_session(self, session_id: str):
        self._ensure(session_id)
        return self.get(session_id)

    # =========================================================
    # SEMANTIC RECALL
    # =========================================================
    def recall(self, session_id: str, query: str, limit=5):
        self._ensure(session_id)

        words = query.lower().split()
        scored = []

        for m in self.data["sessions"][session_id]["messages"]:
            score = sum(m["content"].lower().count(w) for w in words)
            if score > 0:
                scored.append((score, m))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [m for _, m in scored[:limit]]

    # =========================================================
    # COMPRESSION ENGINE (AUTO-SUMMARIZATION)
    # =========================================================
    def _maybe_compress(self, session_id: str):
        session = self.data["sessions"][session_id]
        msgs = session["messages"]

        # threshold trigger
        if len(msgs) < 30:
            return

        # take oldest chunk
        chunk = msgs[:20]
        remaining = msgs[20:]

        summary_text = " ".join(m["content"] for m in chunk)

        # naive compression (LLM-ready hook point)
        existing = session.get("summary", "")
        session["summary"] = (existing + " " + summary_text).strip()[:4000]

        session["messages"] = remaining