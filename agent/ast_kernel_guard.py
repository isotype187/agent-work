import ast
import os

SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "venv",
}


def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def analyze_ast(file_content):
    try:
        tree = ast.parse(file_content)
        return tree
    except Exception:
        return None


def extract_imports(tree):
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)

        if isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


def extract_function_calls(tree):
    calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if hasattr(node.func, "id"):
                calls.append(node.func.id)
            elif hasattr(node.func, "attr"):
                calls.append(node.func.attr)

    return calls


def iter_python_files(path):
    if os.path.isfile(path):
        if path.endswith(".py"):
            yield path
        return

    if not os.path.isdir(path):
        return

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in files:
            if filename.endswith(".py"):
                yield os.path.join(root, filename)


def check_python_file(file_path):
    content = load_file(file_path)
    tree = analyze_ast(content)

    if not tree:
        return [f"{file_path}: Invalid Python AST"]

    imports = extract_imports(tree)
    calls = extract_function_calls(tree)

    issues = []

    # -----------------------------
    # RULE 1: core must not call router directly
    # -----------------------------
    normalized_path = file_path.replace("\\", "/")

    if normalized_path.endswith("core.py"):
        if "router" in imports or "router" in calls:
            issues.append(f"{file_path}: Core layer directly referencing router (architecture violation)")

    # -----------------------------
    # RULE 2: tools must be isolated
    # -----------------------------
    if "/tools/" in normalized_path:
        if "router" in imports:
            issues.append(f"{file_path}: Tool importing router (violates isolation rule)")

    # -----------------------------
    # RULE 3: router must not execute tools directly
    # -----------------------------
    if normalized_path.endswith("router.py"):
        if "subprocess" in imports:
            issues.append(f"{file_path}: Router using subprocess directly (bypasses tool layer)")

    return issues


def run_ast_kernel_check(file_path):
    issues = []

    for python_file in iter_python_files(file_path):
        issues.extend(check_python_file(python_file))

    return {
        "ok": len(issues) == 0,
        "issues": issues
    }
