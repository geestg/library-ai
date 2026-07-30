from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    ROOT / "delbot_platform/research/services/answer.py",
    ROOT / "delbot_platform/application/research/answer.py",
]

for file in FILES:

    code = file.read_text()

    code = code.replace(
        "def answer(",
        "async def answer(",
    )

    code = code.replace(
        ".answer(",
        ".answer(",
    )

    lines = code.splitlines()

    out = []

    for line in lines:

        if "= self.pipeline.answer(" in line and "await" not in line:
            indent = line[:len(line)-len(line.lstrip())]
            rhs = line.split("=",1)[1].strip()
            line = f"{indent}response = await {rhs}"

        elif "return self.service.answer(" in line and "await" not in line:
            indent = line[:len(line)-len(line.lstrip())]
            rhs = line.strip()[7:]
            line = f"{indent}return await {rhs}"

        out.append(line)

    code = "\n".join(out)

    file.write_text(code)

    print("PATCHED")
    print(file)
    print()

print("=" * 72)
print("VERIFY")
print("=" * 72)

for file in FILES:

    tree = ast.parse(file.read_text())

    print(file.name)

    for node in ast.walk(tree):

        if isinstance(node, ast.AsyncFunctionDef):
            print("ASYNC :", node.name)

        if isinstance(node, ast.Await):
            print("AWAIT : line", node.lineno)

    print()
