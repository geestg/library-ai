from __future__ import annotations

import ast
import inspect
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MODULE = "delbot_platform.application.research.answer"

print("=" * 80)
print("APPLICATION ENTRY AUDIT")
print("=" * 80)

try:

    mod = importlib.import_module(MODULE)

    print()
    print("IMPORT : PASS")

except Exception as e:

    print()
    print("IMPORT : FAILED")
    print(e)
    raise

print()

source = Path(mod.__file__)

print("FILE")
print(source)

tree = ast.parse(source.read_text())

print()
print("=" * 80)
print("CLASSES")
print("=" * 80)

for node in tree.body:

    if isinstance(node, ast.ClassDef):

        print()
        print(node.name)

        for item in node.body:

            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):

                kind = "async" if isinstance(item, ast.AsyncFunctionDef) else "sync"

                args = []

                for a in item.args.args:
                    args.append(a.arg)

                print(
                    f"  {kind:5} {item.name}({', '.join(args)})"
                )

print()
print("=" * 80)
print("RUNTIME METHODS")
print("=" * 80)

Application = getattr(mod, "ResearchAnswerApplication")

app = Application()

members = inspect.getmembers(
    app,
    predicate=callable,
)

for name, fn in members:

    if name.startswith("_"):
        continue

    print(
        f"{name:25}",
        "async" if inspect.iscoroutinefunction(fn) else "sync",
    )

print()
print("=" * 80)
print("PUBLIC ATTRIBUTES")
print("=" * 80)

for name in sorted(vars(app).keys()):

    print(name)

print()
print("=" * 80)
print("DONE")
print("=" * 80)
