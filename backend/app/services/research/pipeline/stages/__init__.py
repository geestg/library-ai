from app.services.research.pipeline.registry import (
    registry,
)

from .document_stage import (
    DocumentStage,
)

from .search_stage import (
    SearchStage,
)

from .domain_stage import (
    DomainStage,
)

from .comparison_stage import (
    ComparisonStage,
)

from .evidence_stage import (
    EvidenceStage,
)

from .competency_stage import (
    CompetencyStage,
)

from .prodi_stage import (
    ProdiStage,
)

from .thesis_idea_stage import (
    ThesisIdeaStage,
)

from .context_stage import (
    ContextStage,
)

from .literature_stage import (
    LiteratureStage,
)

from .prompt_stage import (
    PromptStage,
)

from .llm_stage import (
    LLMStage,
)

from .response_stage import (
    ResponseStage,
)


# =====================================
# REGISTER STAGES
# =====================================

registry.register(
    DocumentStage()
)

registry.register(
    SearchStage()
)

registry.register(
    DomainStage()
)

registry.register(
    ComparisonStage()
)

registry.register(
    EvidenceStage()
)

registry.register(
    CompetencyStage()
)

registry.register(
    ProdiStage()
)

registry.register(
    ThesisIdeaStage()
)

registry.register(
    ContextStage()
)

registry.register(
    LiteratureStage()
)

registry.register(
    PromptStage()
)

registry.register(
    LLMStage()
)

registry.register(
    ResponseStage()
)


# =====================================
# EXPORTS
# =====================================

__all__ = [

    "DocumentStage",

    "SearchStage",

    "DomainStage",

    "ComparisonStage",

    "EvidenceStage",

    "CompetencyStage",

    "ProdiStage",

    "ThesisIdeaStage",

    "ContextStage",

    "LiteratureStage",

    "PromptStage",

    "LLMStage",

    "ResponseStage",

]