import ast
import os


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


def run_ast_kernel_check(file_path):
    content = load_file(file_path)
    tree = analyze_ast(content)

    if not tree:
        return {"ok": False, "issues": ["Invalid Python AST"]}

    imports = extract_imports(tree)
    calls = extract_function_calls(tree)

    issues = []

    # -----------------------------
    # RULE 1: core must not call router directly
    # -----------------------------
    if file_path.endswith("core.py"):
        if "router" in imports or "router" in calls:
            issues.append("Core layer directly referencing router (architecture violation)")

    # -----------------------------
    # RULE 2: tools must be isolated
    # -----------------------------
    if "tools" in file_path:
        if "router" in imports:
            issues.append("Tool importing router (violates isolation rule)")

    # -----------------------------
    # RULE 3: router must not execute tools directly
    # -----------------------------
    if file_path.endswith("router.py"):
        if "subprocess" in imports:
            issues.append("Router using subprocess directly (bypasses tool layer)")

    return {
        "ok": len(issues) == 0,
        "issues": issues
    }