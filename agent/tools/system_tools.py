from agent.registry import registry
from agent.runtime import safe_run


def run_cmd(cmd):
    result = safe_run(cmd, shell=True, capture_output=True, text=True)
    return result["stdout"] + result["stderr"]


registry.register("run_cmd", run_cmd)
