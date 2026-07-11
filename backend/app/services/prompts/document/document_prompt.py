from app.services.llm.prompts.base_prompt import (
    BasePrompt,
)

from .principles import PRINCIPLES
from .grounding import GROUNDING
from .output_rules import OUTPUT_RULES


class DocumentPrompt:

    @staticmethod
    def build(

        query: str,

        document_context: str,

    ):

        intro = f"""
Anda adalah DELBot.

==================================================
DOCUMENT CONTEXT
==================================================

{document_context}

==================================================
PERTANYAAN
==================================================

{query}
"""

        return BasePrompt.join(

            intro,

            PRINCIPLES,

            GROUNDING,

            OUTPUT_RULES,

        )