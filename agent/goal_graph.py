import json
import os
import time
import uuid

GRAPH_FILE = "memory/goal_graph.json"


# -----------------------------
# IO LAYER
# -----------------------------
def _load():
    try:
        with open(GRAPH_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save(data):
    os.makedirs(os.path.dirname(GRAPH_FILE), exist_ok=True)

    with open(GRAPH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# -----------------------------
# CORE GOAL API
# -----------------------------
def create_goal(goal, priority=0.5, parent=None):
    graph = _load()

    gid = str(uuid.uuid4())

    graph[gid] = {
        "id": gid,
        "goal": goal,
        "priority": priority,
        "parent": parent,
        "children": [],
        "status": "active",
        "created": time.time()
    }

    if parent and parent in graph:
        graph[parent]["children"].append(gid)

    _save(graph)
    return gid


def get_graph():
    return _load()


def get_ready_goals():
    graph = _load()
    ready = []

    for gid, node in graph.items():

        if node.get("status") != "active":
            continue

        parent = node.get("parent")

        # root nodes always ready
        if not parent:
            ready.append(node)
            continue

        # child only ready if parent done
        parent_node = graph.get(parent)

        if parent_node and parent_node.get("status") == "done":
            ready.append(node)

    ready.sort(key=lambda x: x.get("priority", 0), reverse=True)

    return ready


def complete_goal(goal_id):
    graph = _load()

    if goal_id in graph:
        graph[goal_id]["status"] = "done"

    _save(graph)


# -----------------------------
# STABILITY LAYER (CRITICAL)
# -----------------------------
def decay_graph():
    """
    Soft priority decay over time.
    """
    graph = _load()
    now = time.time()

    for node in graph.values():
        age = now - node.get("created", now)

        # slow decay curve
        decay = min(age / 86400, 0.3)  # cap decay

        node["priority"] = max(
            0.1,
            node.get("priority", 0.5) - decay * 0.05
        )

    _save(graph)


def prune_graph():
    """
    Remove completed goals + fix broken links.
    """
    graph = _load()

    # remove done goals
    graph = {
        k: v for k, v in graph.items()
        if v.get("status") != "done"
    }

    # clean orphan references
    for node in graph.values():
        node["children"] = [
            c for c in node.get("children", [])
            if c in graph
        ]

    _save(graph)


def stabilize_graph():
    """
    Single entry maintenance function.
    """
    decay_graph()
    prune_graph()