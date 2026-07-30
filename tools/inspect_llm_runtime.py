from __future__ import annotations

import ast
import importlib
import inspect
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("=" * 70)
print("LLM RUNTIME")
print("=" * 70)

TARGETS = [
    "delbot_platform.knowledge.rag.llm.generator",
    "delbot_platform.knowledge.rag.llm.response",
    "delbot_platform.knowledge.rag.pipeline",
    "delbot_platform.knowledge.rag.rag_engine",
    "delbot_platform.gateway",
    "delbot_platform.gateway.router",
    "delbot_platform.gateway.service",
]

for module_name in TARGETS:

    print()
    print("=" * 70)
    print(module_name)
    print("=" * 70)

    try:
        module = importlib.import_module(module_name)
    except Exception as e:
        print(type(e).__name__)
        print(e)
        continue

    print("IMPORT : PASS")

    for name, obj in inspect.getmembers(module):

        if inspect.isclass(obj):

            print()
            print("CLASS :", name)

            try:
                print("SIGNATURE :", inspect.signature(obj))
            except Exception:
                pass

            methods = []

            for mname, member in inspect.getmembers(obj):

                if mname.startswith("_"):
                    continue

                if inspect.isfunction(member) or inspect.ismethod(member):
                    methods.append(mname)

            if methods:
                print("METHODS")
                for m in methods:
                    try:
                        sig = inspect.signature(getattr(obj, m))
                    except Exception:
                        sig = "()"
                    print(f"  {m}{sig}")

    print()
    print("SOURCE FILE")
    print(module.__file__)

print()
print("=" * 70)
print("SEARCH generate()/chat()/answer()")
print("=" * 70)

for py in ROOT.rglob("*.py"):

    if ".venv" in py.parts:
        continue

    if "__pycache__" in py.parts:
        continue

    try:
        source = py.read_text(
            encoding="utf-8",
        )
    except Exception:
        continue

    if (
        "generate(" in source
        or "chat(" in source
        or "answer(" in source
    ):

        print(py.relative_to(ROOT))

print()
print("=" * 70)
print("DONE")
print("=" * 70)
