from __future__ import annotations

from delbot_platform.knowledge.models import DocumentChunk


class ContextBuilder:

    def build(
        self,
        results: list[DocumentChunk],
    ) -> str:

        contexts: list[str] = []

        for index, chunk in enumerate(results):

            contexts.append(
                f"""
SOURCE {index + 1}

TITLE:
{chunk.document.title}

FILE:
{chunk.document.file_path}

PAGE:
{chunk.page}

CONTENT:
{chunk.text}
""".strip()
            )

        return "\n\n".join(contexts)