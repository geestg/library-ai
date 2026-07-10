from app.services.research.pipeline.pipeline import (
    ResearchPipeline,
)

from app.services.research.pipeline.hooks import (
    PipelineAction,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)


class PipelineExecutor:

    def __init__(
        self,
        context,
    ):

        self.pipeline = ResearchPipeline(
            context
        )

        self.hooks = []

    # =====================================
    # STAGES
    # =====================================

    def add(
        self,
        stage,
    ):

        self.pipeline.add_stage(
            stage
        )

        return self

    # =====================================
    # HOOKS
    # =====================================

    def add_hook(
        self,
        hook,
    ):

        self.hooks.append(
            hook
        )

        return self

    # =====================================
    # EXECUTE
    # =====================================

    def run(self):

        context = self.pipeline.context

        # =================================
        # INITIALIZE STAGE RESULTS
        # =================================

        if not hasattr(
            context,
            "stage_results",
        ):

            context.stage_results = {}

        # =================================
        # EXECUTION STATE
        # =================================

        stop_pipeline = False

        pending_exception = None

        # =================================
        # BEFORE PIPELINE
        # =================================

        for hook in self.hooks:

            action = hook.before_pipeline(
                context
            )

            if action == PipelineAction.STOP:

                stop_pipeline = True

                break

        # =================================
        # STAGES
        # =================================

        if not stop_pipeline:

            for stage in self.pipeline.stages:

                skip_stage = False

                # =========================
                # BEFORE STAGE
                # =========================

                for hook in self.hooks:

                    action = hook.before_stage(

                        stage,

                        context,

                    )

                    if action == PipelineAction.SKIP:

                        skip_stage = True

                        break

                    if action == PipelineAction.STOP:

                        stop_pipeline = True

                        break

                # =========================
                # STOP BEFORE EXECUTION
                # =========================

                if stop_pipeline:

                    break

                # =========================
                # SKIP CURRENT STAGE
                # =========================

                if skip_stage:

                    continue

                # =========================
                # EXECUTE STAGE
                # =========================

                try:

                    result = stage.run(
                        context
                    )

                    if result is None:

                        result = StageResult()

                    # =====================
                    # RUNTIME STAGE TRACE
                    # =====================

                    print(
                        "[PIPELINE STAGE RESULT]",
                        {
                            "stage":
                                stage.name,

                            "success":
                                result.success,

                            "stop_pipeline":
                                result.stop_pipeline,

                            "skip_remaining":
                                result.skip_remaining,

                            "message":
                                result.message,
                        },
                        flush=True,
                    )

                except Exception as exc:

                    result = StageResult(

                        success=False,

                        stop_pipeline=True,

                        message=str(exc),

                        metadata={

                            "exception_type":
                                type(exc).__name__,

                        },

                    )

                    context.stage_results[
                        stage.name
                    ] = result

                    # =====================
                    # AFTER FAILED STAGE
                    # =====================

                    for hook in self.hooks:

                        hook.after_stage(

                            stage,

                            context,

                            result,

                        )

                    pending_exception = exc

                    stop_pipeline = True

                    break

                # =========================
                # SAVE RESULT
                # =========================

                context.stage_results[
                    stage.name
                ] = result

                # =========================
                # AFTER STAGE
                # =========================

                for hook in self.hooks:

                    action = hook.after_stage(

                        stage,

                        context,

                        result,

                    )

                    if action == PipelineAction.STOP:

                        stop_pipeline = True

                        break

                # =========================
                # STOP AFTER STAGE HOOK
                # =========================

                if stop_pipeline:

                    break

                # =========================
                # STOP PIPELINE GRACEFULLY
                # =========================

                if result.stop_pipeline:

                    break

                # =========================
                # SKIP REMAINING STAGES
                # =========================

                if result.skip_remaining:

                    break

        # =================================
        # AFTER PIPELINE
        # =================================

        for hook in self.hooks:

            action = hook.after_pipeline(
                context
            )

            if action == PipelineAction.STOP:

                break

        # =================================
        # RERAISE STAGE EXCEPTION
        # =================================

        if pending_exception is not None:

            raise pending_exception

        # =================================
        # DONE
        # =================================

        return context