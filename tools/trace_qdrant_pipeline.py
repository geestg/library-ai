from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    ROOT / "delbot_platform/documents/pipeline/indexing.py",
    ROOT / "delbot_platform/documents/services/indexing.py",
    ROOT / "delbot_platform/documents/embedding/pipeline/pipeline.py",
    ROOT / "delbot_platform/documents/embedding/mapper/vector_mapper.py",
    ROOT / "delbot_platform/vectorstore/qdrant/client.py",
]

TARGET_CALLS = {
    "EmbeddingPipeline",
    "EmbeddingVectorMapper",
    "QdrantVectorStore",
    "upsert",
    "to_vector_record",
    "to_vector_records",
    "create_collection",
    "collection_exists",
    "index",
}


class Visitor(ast.NodeVisitor):

    def __init__(self):
        self.calls = []
        self.classes = []
        self.functions = []

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):

        name = None

        if isinstance(node.func, ast.Name):
            name = node.func.id

        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr

        if name:
            self.calls.append(name)

        self.generic_visit(node)


print("=" * 70)
print("PIPELINE TRACE")
print("=" * 70)

for file in FILES:

    print()
    print("-" * 70)
    print(file.relative_to(ROOT))
    print("-" * 70)

    if not file.exists():
        print("FILE NOT FOUND")
        continue

    tree = ast.parse(file.read_text(encoding="utf-8"))

    visitor = Visitor()
    visitor.visit(tree)

    print()
    print("CLASSES")
    print("-------")

    for c in visitor.classes:
        print(c)

    print()
    print("FUNCTIONS")
    print("---------")

    for f in visitor.functions:
        print(f)

    print()
    print("IMPORTANT CALLS")
    print("---------------")

    found = False

    for c in visitor.calls:
        if c in TARGET_CALLS:
            found = True
            print(c)

    if not found:
        print("NONE")

print()
print("=" * 70)
print("TRACE COMPLETE")
print("=" * 70)
