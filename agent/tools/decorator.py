def tool(name: str | None = None):
    def wrapper(fn):
        fn._is_tool = True
        fn._tool_name = name or fn.__name__
        return fn
    return wrapper