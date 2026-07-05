from dataclasses import dataclass
from dataclasses import field

from datetime import datetime
from datetime import timezone

from typing import Any


# =====================================
# EXECUTION SESSION
# =====================================

@dataclass
class ExecutionSession:

    # =================================
    # REQUEST
    # =================================

    last_query: str = ""

    mode: str = ""

    # =================================
    # MODEL
    # =================================

    provider: str = ""

    model: str = ""

    intent: str = ""

    # =================================
    # RESPONSE
    # =================================

    response: str = ""

    # =================================
    # SNAPSHOT
    # =================================

    serialized_context: dict[
        str,
        Any,
    ] = field(
        default_factory=dict
    )

    # =================================
    # METADATA
    # =================================

    updated_at: datetime | None = None

    # =================================
    # UPDATE FROM RESEARCH CONTEXT
    # =================================

    def update(
        self,
        context,
        serialized_context: dict,
    ):

        self.last_query = (
            context.query
        )

        self.mode = (
            context.mode
        )

        self.provider = (
            context.provider
        )

        self.model = (
            context.model
        )

        self.intent = (
            context.intent
        )

        self.response = (
            context.analysis
        )

        self.serialized_context = (
            serialized_context
        )

        self.updated_at = (
            datetime.now(
                timezone.utc
            )
        )

    # =================================
    # CLEAR
    # =================================

    def clear(self):

        self.last_query = ""

        self.mode = ""

        self.provider = ""

        self.model = ""

        self.intent = ""

        self.response = ""

        self.serialized_context = {}

        self.updated_at = None

    # =================================
    # SERIALIZE
    # =================================

    def to_dict(self):

        return {

            "last_query":
                self.last_query,

            "mode":
                self.mode,

            "provider":
                self.provider,

            "model":
                self.model,

            "intent":
                self.intent,

            "response":
                self.response,

            "updated_at":
                (
                    self.updated_at.isoformat()
                    if self.updated_at
                    else None
                ),

            "serialized_context":
                self.serialized_context,

        }