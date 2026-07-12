from app.services.prompts.base_prompt import (
    BasePrompt,
)


class PromptComposer:

    @staticmethod
    def compose(
        *sections: str,
    ) -> str:

        return BasePrompt.join(
            *sections
        )