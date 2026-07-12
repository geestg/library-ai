from app.services.research.models.research_context import (
    ResearchContext,
)


# =====================================
# SERIALIZER SCHEMA VERSION
# =====================================

SERIALIZER_VERSION = 1


# =====================================
# RESEARCH CONTEXT SERIALIZER
# =====================================

def serialize_research_context(
    context: ResearchContext,
) -> dict:
    """
    Serialize ResearchContext menjadi
    payload standar yang dikirim ke frontend.

    Serializer ini merupakan Single Source
    of Truth untuk seluruh consumer:

    - REST API
    - Streaming API
    - Workspace
    - Session Persistence
    - Future Database Snapshot
    - Export

    Semua consumer harus menggunakan
    serializer ini secara langsung.
    """

    profile = (
        context.research_profile.to_dict()
    )

    return {

        # =================================
        # PAYLOAD METADATA
        # =================================

        "schema": {

            "name":
                "research_context",

            "version":
                SERIALIZER_VERSION,

        },

        # =================================
        # REQUEST
        # =================================

        "query":
            context.query,

        "mode":
            context.mode,

        # =================================
        # MODEL
        # =================================

        "provider":
            context.provider,

        "model":
            context.model,

        "intent":
            context.intent,

        # =================================
        # GENERATED RESPONSE
        # =================================

        "analysis":
            context.analysis,

        # =================================
        # DOMAIN MODEL
        # =================================

        "research_profile":
            profile,

        # =================================
        # RETRIEVAL
        # =================================

        "sources":
            context.theses,

        "citations":
            context.citations,

        # =================================
        # EVIDENCE
        # =================================

        "evidence":
            context.evidence,

        "evidence_matrix":
            context.evidence_matrix,

        # =================================
        # PIPELINE
        # =================================

        "pipeline": {

            "stages": {

                stage: {

                    "success":
                        result.success,

                    "duration_ms":
                        result.duration_ms,

                    "message":
                        result.message,

                    "metadata":
                        result.metadata,

                }

                for stage, result in
                context.stage_results.items()

            }

        },

    }

