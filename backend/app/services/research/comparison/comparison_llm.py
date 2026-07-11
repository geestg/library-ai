from app.services.llm.model_gateway import (
    gateway
)

from app.services.llm.generation_profiles import (
    GenerationProfiles,
)

def generate_comparison_analysis(
    prompt: str
):

    return gateway.generate_response(

        prompt=prompt,

        **GenerationProfiles.ANSWER,

    )