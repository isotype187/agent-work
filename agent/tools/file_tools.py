from registry import registry

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"written: {path}"


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


registry.register("write_file", write_file)
registry.register("read_file", read_file)