from collections.abc import Callable

from app.services.research.pipeline.base_hook import (
    BasePipelineHook,
)

from app.services.research.pipeline.hooks import (
    PipelineAction,
)


# =====================================
# STAGE PHASE MAP
# =====================================

STAGE_PHASES = {

    "document": {

        "phase":
            "reading_documents",

        "label":
            "Membaca dokumen",

    },

    "search": {

        "phase":
            "searching_knowledge",

        "label":
            "Mencari pengetahuan relevan",

    },

    "domain": {

        "phase":
            "understanding_domain",

        "label":
            "Memahami domain penelitian",

    },

    "comparison": {

        "phase":
            "comparing_research",

        "label":
            "Membandingkan penelitian",

    },

    "evidence": {

        "phase":
            "analyzing_evidence",

        "label":
            "Menganalisis bukti",

    },

    "competency": {

        "phase":
            "analyzing_competency",

        "label":
            "Menganalisis kompetensi",

    },

    "prodi": {

        "phase":
            "analyzing_academic_context",

        "label":
            "Memahami konteks akademik",

    },

    "thesis_idea": {

        "phase":
            "developing_research_idea",

        "label":
            "Mengembangkan ide penelitian",

    },

    "context": {

        "phase":
            "understanding_context",

        "label":
            "Memahami konteks percakapan",

    },

    "literature": {

        "phase":
            "reviewing_literature",

        "label":
            "Meninjau literatur",

    },

    "prompt": {

        "phase":
            "preparing_response",

        "label":
            "Menyiapkan jawaban",

    },

    "llm": {

        "phase":
            "generating_response",

        "label":
            "Menyusun jawaban",

    },

    "response": {

        "phase":
            "finalizing_response",

        "label":
            "Menyelesaikan jawaban",

    },

}


# =====================================
# STREAM PROGRESS HOOK
# =====================================

class StreamProgressHook(
    BasePipelineHook
):

    def __init__(
        self,
        callback: Callable | None = None,
    ):

        self.callback = callback

        self.last_phase = None

    # =================================
    # EMIT
    # =================================

    def emit(
        self,
        data: dict,
    ):

        if self.callback is None:

            return

        self.callback(
            data
        )

    # =================================
    # BEFORE PIPELINE
    # =================================

    def before_pipeline(
        self,
        context,
    ):

        self.emit({

            "phase":
                "understanding_request",

            "label":
                "Memahami pertanyaan",

            "stage":
                None,

        })

        return PipelineAction.CONTINUE

    # =================================
    # BEFORE STAGE
    # =================================

    def before_stage(
        self,
        stage,
        context,
    ):

        stage_name = getattr(
            stage,
            "name",
            "",
        )

        phase_config = (
            STAGE_PHASES.get(
                stage_name
            )
        )

        if phase_config is None:

            return PipelineAction.CONTINUE

        phase = phase_config[
            "phase"
        ]

        # =================================
        # DUPLICATE PHASE GUARD
        # =================================

        if phase == self.last_phase:

            return PipelineAction.CONTINUE

        self.last_phase = phase

        self.emit({

            "phase":
                phase,

            "label":
                phase_config[
                    "label"
                ],

            "stage":
                stage_name,

        })

        return PipelineAction.CONTINUE