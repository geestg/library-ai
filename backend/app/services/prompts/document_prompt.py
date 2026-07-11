from app.services.llm.prompts.base_prompt import (
    BasePrompt,
)

from app.services.llm.prompts.sections import (
    LANGUAGE_RULES,
    GROUNDING_RULES,
    NO_INTERNAL_REASONING,
)


class DocumentPrompt:

    @staticmethod
    def build(

        query: str,

        document_context: str,

    ):

        intro = f"""
Anda adalah DELBot.

Jawab pertanyaan user hanya berdasarkan
dokumen aktif.

==================================================
DOCUMENT CONTEXT
==================================================

{document_context}

==================================================
PERTANYAAN USER
==================================================

{query}
"""

        task = """
...
aturan document khusus...
"""

        return BasePrompt.join(

            intro,

            GROUNDING_RULES,

            task,

            NO_INTERNAL_REASONING,

            LANGUAGE_RULES,

        )