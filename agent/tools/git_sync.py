import subprocess

def run(cmd):
    return subprocess.run(cmd, text=True)

def sync():
    run(["git", "add", "."])
    run(["git", "commit", "-m", "sync: agent state update"])
    run(["git", "pull", "origin", "main", "--rebase"])
    run(["git", "push", "origin", "main"])

if __name__ == "__main__":
    sync()