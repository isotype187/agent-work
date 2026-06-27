import subprocess

class GitSafeTool:
    def run(self, cmd):
        return subprocess.run(cmd, text=True, capture_output=True)

    def pull(self):
        print("🔄 Pulling from origin...")
        return self.run(["git", "pull", "origin", "main", "--rebase"])

    def push(self):
        print("🚀 Pushing to origin...")
        return self.run(["git", "push", "origin", "main"])

    def sync(self):
        print("🧠 Safe Git Sync Starting...")

        pull_result = self.pull()
        if pull_result.returncode != 0:
            print("⚠️ Pull failed:")
            print(pull_result.stderr)
            return

        push_result = self.push()
        if push_result.returncode != 0:
            print("⚠️ Push failed:")
            print(push_result.stderr)
            return

        print("✅ Sync complete")