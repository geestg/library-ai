from app.services.prompts.base_prompt import (
    BasePrompt,
)

from .principles import PRINCIPLES
from .grounding import GROUNDING
from .completeness import COMPLETENESS
from .scope import SCOPE
from .uncertainty import UNCERTAINTY
from .format_rules import FORMAT_RULES
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

        return PromptComposer.compose(

            intro,

            PRINCIPLES,

            GROUNDING,

            COMPLETENESS,

            SCOPE,

            UNCERTAINTY,

            FORMAT_RULES,

            OUTPUT_RULES,

        )