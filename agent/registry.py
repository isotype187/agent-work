class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, func):
        """Register a tool by name with a function."""
        self.tools[name] = func

    def run(self, name, *args, **kwargs):
        """Run a registered tool by name, passing arguments."""
        if name not in self.tools:
            raise Exception(f"Tool not found: {name}")
        return self.tools[name](*args, **kwargs)

# Create a single instance of the registry
registry = ToolRegistry()