from __future__ import annotations

from pathlib import Path
import ast
import py_compile

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    ROOT / "delbot_platform/research/services/answer.py",
    ROOT / "delbot_platform/application/research/answer.py",
]

print("=" * 72)
print("REPAIR")
print("=" * 72)

for file in FILES:

    code = file.read_text()

    while "async async" in code:
        code = code.replace("async async", "async")

    while "async  async" in code:
        code = code.replace("async  async", "async")

    while "async   async" in code:
        code = code.replace("async   async", "async")

    file.write_text(code)

    print("FIXED :", file)

print()
print("=" * 72)
print("AST VERIFY")
print("=" * 72)

for file in FILES:

    try:
        ast.parse(file.read_text())
        print("PASS :", file)

    except Exception as e:
        print("FAIL :", file)
        print(e)

print()
print("=" * 72)
print("PY_COMPILE")
print("=" * 72)

for file in FILES:

    try:
        py_compile.compile(str(file), doraise=True)
        print("PASS :", file)

    except Exception as e:
        print("FAIL :", file)
        print(e)

print()
print("=" * 72)
print("VERIFY")
print("=" * 72)

for file in FILES:

    print()
    print(file)

    lines = file.read_text().splitlines()

    for i, line in enumerate(lines, 1):

        if "async def answer" in line:
            print(f"{i}: {line}")

        if "return await" in line:
            print(f"{i}: {line}")

        if "await self.pipeline.answer" in line:
            print(f"{i}: {line}")

        if "await self.service.answer" in line:
            print(f"{i}: {line}")

