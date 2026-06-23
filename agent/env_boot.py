import os
import sys


def load_project_root():
    """
    Forces the runtime working directory to project root
    so all relative paths (memory/, config/, logs/) work correctly.
    """

    current_file = os.path.abspath(__file__)

    # go up from agent/env_boot.py → project root
    project_root = os.path.abspath(os.path.join(current_file, "..", ".."))

    os.chdir(project_root)

    # ensure root is in python path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    return project_root