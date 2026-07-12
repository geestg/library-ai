from app.services.research.models.research_context import (
    ResearchContext,
)

from app.services.research.serializers import (
    serialize_research_context,
)


# =====================================
# RESEARCH RESPONSE ENGINE
# =====================================

def build_research_response(
    context: ResearchContext,
) -> dict:
    """
    Build standardized research response.

    Seluruh consumer menggunakan payload
    yang dihasilkan oleh serializer sebagai
    Single Source of Truth.
    """

    # =====================================
    # SERIALIZE CONTEXT
    # =====================================

    response = serialize_research_context(
        context
    )

    # =====================================
    # LEGACY COMPATIBILITY
    # =====================================

    profile = response.get(
        "research_profile",
        {},
    )

    response.update({

        "trend_analysis":
        profile.get(
            "trend",
            {},
        ),

        "gap_analysis":
        profile.get(
            "gap",
            {},
        ),

        "novelty_analysis":
        profile.get(
            "novelty",
            {},
        ),

        "competency_analysis":
        profile.get(
            "competency",
            {},
        ),

        "prodi_analysis":
        profile.get(
            "prodi",
            {},
        ),

    })

    return response

