from app.services.research.pipeline import (
    PipelineExecutor,
)

from app.services.research.pipeline.stream_progress_hook import (
    StreamProgressHook,
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

        progress_callback=None,

    ):

        # =====================================
        # ATTACH RUNTIME STREAM MODE
        # =====================================

        context.stream = stream

        # =====================================
        # ATTACH RUNTIME PROGRESS CALLBACK
        # =====================================

        context.progress_callback = (
            progress_callback
        )

        # =====================================
        # EXECUTOR
        # =====================================

        executor = PipelineExecutor(
            context
        )

        # =====================================
        # STREAM PROGRESS HOOK
        # =====================================

        if progress_callback is not None:

            executor.add_hook(

                StreamProgressHook(

                    callback=(
                        progress_callback
                    ),

                )

            )

        # =====================================
        # DOCUMENT
        # =====================================

        executor.add(

            DocumentStage(

                stream=stream,

            )

        )

        # =====================================
        # SEARCH
        # =====================================

        executor.add(

            SearchStage()

        )

        # =====================================
        # DOMAIN
        # =====================================

        executor.add(

            DomainStage()

        )

        # =====================================
        # COMPARISON
        # =====================================

        executor.add(

            ComparisonStage()

        )

        # =====================================
        # EVIDENCE
        # =====================================

        executor.add(

            EvidenceStage()

        )

        # =====================================
        # COMPETENCY
        # =====================================

        executor.add(

            CompetencyStage()

        )

        # =====================================
        # PRODI
        # =====================================

        executor.add(

            ProdiStage()

        )

        # =====================================
        # THESIS IDEA
        # =====================================

        executor.add(

            ThesisIdeaStage()

        )

        # =====================================
        # CONTEXT
        # =====================================

        executor.add(

            ContextStage()

        )

        # =====================================
        # LITERATURE REVIEW
        # =====================================

        executor.add(

            LiteratureStage()

        )

        # =====================================
        # PROMPT
        # =====================================

        executor.add(

            PromptStage()

        )

        # =====================================
        # LLM
        # =====================================

        executor.add(

            LLMStage(

                stream=stream,

            )

        )

        # =====================================
        # RESPONSE
        # =====================================

        executor.add(

            ResponseStage()

        )

        return executor