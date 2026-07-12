from app.services.llm.generation_profiles import (
    GenerationProfiles,
)

from app.services.prompts.models.prompt_type import (
    PromptType,
)


class GenerationProfileResolver:

    _profiles = {

        PromptType.ANSWER:
            GenerationProfiles.ANSWER,

        PromptType.DOCUMENT:
            GenerationProfiles.ANSWER,

        PromptType.VERIFIER:
            GenerationProfiles.VERIFIER,

        PromptType.QUERY_RESOLUTION:
            GenerationProfiles.QUERY_RESOLUTION,

        PromptType.RESEARCH:
            GenerationProfiles.RESEARCH,

        PromptType.CREATIVE:
            GenerationProfiles.CREATIVE,

        PromptType.TITLE:
            GenerationProfiles.TITLE,

    }

    @classmethod
    def resolve(
        cls,
        prompt_type: PromptType,
    ) -> dict:

        try:

            return cls._profiles[
                prompt_type
            ]

        except KeyError as exc:

            raise ValueError(

                f"No generation profile "
                f"registered for "
                f"{prompt_type.value}"

            ) from exc