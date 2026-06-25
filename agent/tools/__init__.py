def tool(name=None):
    """
    Marks a function as a plugin tool.
    """

    def wrapper(fn):
        fn._is_tool = True
        fn._tool_name = name or fn.__name__
        return fn

    return wrapper