from app.services.prompts.base_prompt import (
    BasePrompt,
)

from app.services.prompts.composer import (
    PromptComposer,
)

from .intro import (
    INTRO_TEMPLATE,
)

from .language_rules import (
    LANGUAGE_RULES,
)

from .answer_rules import (
    ANSWER_RULES,
)

from .citation_rules import (
    CITATION_RULES,
)

from .output_rules import (
    OUTPUT_RULES,
)

from .mode_detector import (
    detect_response_mode,
)


class AnswerPrompt:

    @staticmethod
    def build(
        *,
        query: str,
        context: str,
        intent: str,
    ) -> str:

        mode, mode_instruction = (
            detect_response_mode(
                query
            )
        )

        intro = INTRO_TEMPLATE.format(

            query=query,

            context=context,

            intent=intent,

            mode=mode,

            mode_instruction=mode_instruction,

        )

        return PromptComposer.compose(

            intro,

            LANGUAGE_RULES,

            ANSWER_RULES,

            CITATION_RULES,

            OUTPUT_RULES,

        )
