from agent.executor import run
from agent.registry import registry


def run_cmd(cmd):
    result = run(cmd)
    return (result.get("stdout") or "") + (result.get("stderr") or "")


registry.register("run_cmd", run_cmd)
