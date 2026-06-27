import io
import unittest
from contextlib import redirect_stdout

from agent.auto_commit import auto_commit_enabled, safe_commit
from agent.router import detect_intent, route_request, select_tool
from agent.tools.git_tool import git_status


class RouterToolTests(unittest.TestCase):
    def test_status_routes_to_git_status_tool(self):
        self.assertEqual(select_tool("git status"), "git_status")
        self.assertEqual(detect_intent("git status"), "tool")

    def test_route_request_executes_registered_status_tool(self):
        tools = {"git_status": lambda payload: {"status": "ok", "payload": payload}}

        result = route_request("git status", tools=tools, profile={})

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["payload"], "git status")


class GitToolTests(unittest.TestCase):
    def test_git_status_returns_stable_shape(self):
        result = git_status()

        self.assertEqual(result["status"], "success")
        self.assertIn("output", result)
        self.assertIsInstance(result["output"], str)


class AutoCommitSafetyTests(unittest.TestCase):
    def test_auto_commit_is_disabled_by_default_config(self):
        self.assertFalse(auto_commit_enabled())

    def test_safe_commit_blocks_when_disabled(self):
        output = io.StringIO()

        with redirect_stdout(output):
            safe_commit()

        self.assertIn("AUTO-COMMIT BLOCK", output.getvalue())


if __name__ == "__main__":
    unittest.main()
