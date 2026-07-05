from app.services.research.pipeline import (
    PipelineExecutor,
)

from app.services.research.pipeline.stages import (

    DocumentStage,

    SearchStage,

    DomainStage,

    ComparisonStage,

    EvidenceStage,

    CompetencyStage,

    ProdiStage,

    ThesisIdeaStage,

    ContextStage,

    LiteratureStage,

    PromptStage,

    LLMStage,

    ResponseStage,

)


class ResearchPipelineBuilder:

    """
    Builder untuk pipeline utama.

    Seluruh urutan stage didefinisikan
    hanya di sini.
    """

    @staticmethod
    def build(

        context,

        stream: bool = False,

    ):

        return (

            PipelineExecutor(context)

            # =====================================
            # DOCUMENT
            # =====================================

            .add(

                DocumentStage()

            )

            # =====================================
            # SEARCH
            # =====================================

            .add(

                SearchStage()

            )

            # =====================================
            # DOMAIN
            # =====================================

            .add(

                DomainStage()

            )

            # =====================================
            # COMPARISON
            # =====================================

            .add(

                ComparisonStage()

            )

            # =====================================
            # EVIDENCE
            # =====================================

            .add(

                EvidenceStage()

            )

            # =====================================
            # COMPETENCY
            # =====================================

            .add(

                CompetencyStage()

            )

            # =====================================
            # PRODI
            # =====================================

            .add(

                ProdiStage()

            )

            # =====================================
            # THESIS IDEA
            # =====================================

            .add(

                ThesisIdeaStage()

            )

            # =====================================
            # CONTEXT
            # =====================================

            .add(

                ContextStage()

            )

            # =====================================
            # LITERATURE REVIEW
            # =====================================

            .add(

                LiteratureStage()

            )

            # =====================================
            # PROMPT
            # =====================================

            .add(

                PromptStage()

            )

            # =====================================
            # LLM
            # =====================================

            .add(

                LLMStage(

                    stream=stream,

                )

            )

            # =====================================
            # RESPONSE
            # =====================================

            .add(

                ResponseStage()

            )

        )