from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

file = ROOT / "delbot_platform/research/pipeline/research_answer_pipeline.py"

new_code = """from __future__ import annotations

from delbot_platform.knowledge.rag.pipeline import RAGPipeline
from delbot_platform.research.generator import LLMGenerator
from delbot_platform.research.prompt_builder import (
    ResearchPromptBuilder,
)


class ResearchAnswerPipeline:

    def __init__(
        self,
    ) -> None:

        self.rag = RAGPipeline()

        self.prompt_builder = ResearchPromptBuilder()

        self.generator = LLMGenerator()

    def answer(
        self,
        *,
        question: str,
        history: list[dict] | None = None,
        previous: str = "",
        research_state: dict | None = None,
    ):

        history = history or []

        research_state = research_state or {}

        rag = self.rag.build(
            query=question,
        )

        messages = self.prompt_builder.build(
            query=question,
            context=rag.context,
            history=history,
            previous=previous,
            research_state=research_state,
        )

        answer = self.generator.generate(
            messages,
        )

        return answer, rag
"""

file.write_text(new_code, encoding="utf-8")

print()
print("PATCHED")
print(file)
