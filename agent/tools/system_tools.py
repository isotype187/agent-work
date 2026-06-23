import subprocess
from registry import registry


def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr


registry.register("run_cmd", run_cmd)