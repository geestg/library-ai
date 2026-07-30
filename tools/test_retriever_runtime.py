from __future__ import annotations

import ast
import asyncio
import importlib
import inspect
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


QUERY = "PLC OMRON CPM2A dan Arduino Mega 2560"


def locate_retriever():

    candidates = [
        (
            "delbot_platform.knowledge.retrieval.qdrant",
            [
                "QdrantRetriever",
                "QdrantRetrieval",
                "QdrantSearch",
            ],
        ),
        (
            "delbot_platform.knowledge.retrieval.retriever",
            [
                "Retriever",
                "KnowledgeRetriever",
                "DocumentRetriever",
            ],
        ),
        (
            "delbot_platform.knowledge.rag.vector_retriever",
            [
                "VectorRetriever",
                "QdrantRetriever",
            ],
        ),
    ]

    for module_name, class_names in candidates:

        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue

        for class_name in class_names:

            if hasattr(module, class_name):
                return (
                    module_name,
                    class_name,
                    getattr(module, class_name),
                )

    return (
        None,
        None,
        None,
    )


def discover_public_methods(cls):

    methods = []

    for name, func in inspect.getmembers(
        cls,
        inspect.isfunction,
    ):

        if name.startswith("_"):
            continue

        methods.append(name)

    return methods


async def invoke(instance):

    preferred = [
        "retrieve",
        "search",
        "query",
        "run",
    ]

    for name in preferred:

        if not hasattr(instance, name):
            continue

        method = getattr(instance, name)

        try:

            signature = inspect.signature(method)

            kwargs = {}

            for parameter in list(signature.parameters.values()):

                if parameter.name == "self":
                    continue

                if parameter.name in (
                    "query",
                    "text",
                ):
                    kwargs[parameter.name] = QUERY

                elif parameter.name in (
                    "top_k",
                    "k",
                    "limit",
                ):
                    kwargs[parameter.name] = 5

            started = time.perf_counter()

            if inspect.iscoroutinefunction(method):
                result = await method(**kwargs)
            else:
                result = method(**kwargs)

            elapsed = time.perf_counter() - started

            return (
                name,
                result,
                elapsed,
                None,
            )

        except Exception as exc:

            return (
                name,
                None,
                None,
                exc,
            )

    return (
        None,
        None,
        None,
        RuntimeError("No callable retrieval method"),
    )


async def main():

    print("=" * 70)
    print("LOCATE RETRIEVER")
    print("=" * 70)

    module_name, class_name, cls = locate_retriever()

    if cls is None:
        print("RETRIEVER NOT FOUND")
        return

    print("MODULE :", module_name)
    print("CLASS  :", class_name)

    print()
    print("=" * 70)
    print("PUBLIC METHODS")
    print("=" * 70)

    methods = discover_public_methods(cls)

    for method in methods:
        print(method)

    print()
    print("=" * 70)
    print("CREATE INSTANCE")
    print("=" * 70)

    instance = cls()

    print(type(instance).__name__)

    print()
    print("=" * 70)
    print("RUN")
    print("=" * 70)

    method, result, elapsed, error = await invoke(instance)

    if error is not None:

        print("METHOD :", method)
        print("STATUS : FAILED")
        print(type(error).__name__)
        print(error)

        return

    print("METHOD :", method)
    print("STATUS : PASS")

    if elapsed is not None:
        print(f"TIME   : {elapsed:.2f}s")

    print()

    if isinstance(result, list):

        print("=" * 70)
        print("RESULT")
        print("=" * 70)

        print("COUNT :", len(result))

        for i, item in enumerate(result[:5], start=1):

            print("-" * 70)
            print(f"TOP {i}")

            if hasattr(item, "__dict__"):

                for key, value in vars(item).items():

                    if key == "text" and isinstance(value, str):
                        value = value[:300]

                    print(f"{key:15}: {value}")

            else:

                print(item)

    else:

        print("=" * 70)
        print("RETURN TYPE")
        print("=" * 70)

        print(type(result))
        print(result)


asyncio.run(main())

