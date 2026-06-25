import importlib
import pkgutil


class ToolRegistry:
    """
    Central plugin-based tool system.
    Auto-loads tools + supports manual registration.
    """

    def __init__(self):
        self.tools = {}

    # -----------------------------
    # CORE API
    # -----------------------------
    def register(self, name: str, fn):
        self.tools[name] = fn

    def get(self, name: str):
        return self.tools.get(name)

    def has(self, name: str):
        return name in self.tools

    def all(self):
        return dict(self.tools)

    # -----------------------------
    # AUTO PLUGIN LOADER
    # -----------------------------
    def load_plugins(self, package: str = "agent.tools"):
        """
        Auto-imports modules inside agent/tools/
        and registers @tool-decorated functions.
        """

        pkg = importlib.import_module(package)

        for _, module_name, _ in pkgutil.iter_modules(pkg.__path__):
            module = importlib.import_module(f"{package}.{module_name}")

            for attr_name in dir(module):
                obj = getattr(module, attr_name)

                if callable(obj) and getattr(obj, "_is_tool", False):
                    tool_name = getattr(obj, "_tool_name", obj.__name__)
                    self.register(tool_name, obj)


# -----------------------------
# SINGLE GLOBAL REGISTRY
# -----------------------------
registry = ToolRegistry()