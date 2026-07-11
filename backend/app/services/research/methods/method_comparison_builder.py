from app.services.research.methods.method_knowledge import (
    METHOD_KNOWLEDGE
)


def build_method_entry(
    method_name: str,
    frequency: int
):

    metadata = METHOD_KNOWLEDGE.get(

        method_name.lower(),

        {

            "interpretability":
            "Tidak diketahui",

            "complexity":
            "Tidak diketahui",

            "advantages": [],

            "limitations": [],

            "recommended_scenarios": []
        }
    )

    return {

        "method":
        method_name,

        "frequency":
        frequency,

        "interpretability":
        metadata["interpretability"],

        "complexity":
        metadata["complexity"],

        "advantages":
        metadata["advantages"],

        "limitations":
        metadata["limitations"],

        "recommended_scenarios":
        metadata["recommended_scenarios"]
    }
