from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "delbot_platform/knowledge/rag/pipeline.py",
    "delbot_platform/knowledge/rag/rag_engine.py",
    "delbot_platform/knowledge/rag/llm/generator.py",
    "delbot_platform/application/research/answer.py",
    "delbot_platform/research/services/answer.py",
    "delbot_platform/research/pipeline/research_answer_pipeline.py",
    "delbot_platform/gateway/services/gateway.py",
    "delbot_platform/gateway/routers/chat.py",
    "delbot_platform/gateway/routers/v1/chat.py",
]

KEYWORDS = [
    "LLMGenerator",
    "generate(",
    "chat(",
    "RAGPipeline",
    "RAGResponse",
    "context",
    "citations",
    "answer",
]


def header(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def walk_calls(tree):
    calls = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node):
            try:
                if isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                elif isinstance(node.func, ast.Name):
                    name = node.func.id
                else:
                    name = ast.dump(node.func)
                calls.append((name, node.lineno))
            except Exception:
                pass
            self.generic_visit(node)

    Visitor().visit(tree)
    return calls


for file in FILES:

    path = ROOT / file

    header(file)

    if not path.exists():
        print("NOT FOUND")
        continue

    print("FILE :", path)

    src = path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(src)
        print("AST : PASS")
    except Exception as e:
        print("AST : FAIL")
        print(e)
        continue

    imports = []

    for node in tree.body:

        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)

        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for n in node.names:
                imports.append(f"{mod}.{n.name}")

    print()
    print("IMPORTS")

    if imports:
        for x in sorted(imports):
            print(" ", x)
    else:
        print("  <none>")

    print()
    print("CLASSES")

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            print(" ", node.name)

    print()
    print("FUNCTIONS")

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            print(" ", node.name)

    print()
    print("CALLS")

    seen = set()

    for name, line in walk_calls(tree):
        if name in seen:
            continue
        seen.add(name)
        print(f"  {name:<25} line {line}")

    print()
    print("KEYWORD SCAN")

    for k in KEYWORDS:
        if k in src:
            print("  FOUND :", k)

print()
print("=" * 72)
print("PIPELINE ENTRY SEARCH")
print("=" * 72)

for py in ROOT.rglob("*.py"):

    if ".venv" in str(py):
        continue

    if "__pycache__" in str(py):
        continue

    try:
        text = py.read_text(encoding="utf-8")
    except Exception:
        continue

    if "LLMGenerator(" in text:
        print(py.relative_to(ROOT))

print()
print("=" * 72)
print("GENERATE() CALL SEARCH")
print("=" * 72)

for py in ROOT.rglob("*.py"):

    if ".venv" in str(py):
        continue

    if "__pycache__" in str(py):
        continue

    try:
        text = py.read_text(encoding="utf-8")
    except Exception:
        continue

    if ".generate(" in text:
        print(py.relative_to(ROOT))

print()
print("=" * 72)
print("CHAT() CALL SEARCH")
print("=" * 72)

for py in ROOT.rglob("*.py"):

    if ".venv" in str(py):
        continue

    if "__pycache__" in str(py):
        continue

    try:
        text = py.read_text(encoding="utf-8")
    except Exception:
        continue

    if ".chat(" in text:
        print(py.relative_to(ROOT))

print()
print("=" * 72)
print("DONE")
print("=" * 72)
