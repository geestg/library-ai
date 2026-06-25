from app.services.llm.model_gateway import (
    gateway
)


def generate_comparison_analysis(
    prompt: str
):

    return gateway.generate_response(
        prompt=prompt
    )