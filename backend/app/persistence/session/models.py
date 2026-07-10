from datetime import datetime
from datetime import timezone

from sqlalchemy import (
    DateTime,
    String,
)

from sqlalchemy.dialects.postgresql import (
    JSONB,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import (
    Base,
)


# =====================================
# WORKSPACE SESSION RECORD
# =====================================

class WorkspaceSessionRecord(
    Base
):

    __tablename__ = (
        "workspace_sessions"
    )

    # =================================
    # SESSION ID
    # =================================

    session_id: Mapped[str] = (
        mapped_column(

            String(64),

            primary_key=True,

        )
    )

    # =================================
    # CONVERSATION
    # =================================

    conversation_data: Mapped[dict] = (
        mapped_column(

            JSONB,

            nullable=False,

            default=dict,

        )
    )

    # =================================
    # DOCUMENTS
    # =================================

    documents_data: Mapped[dict] = (
        mapped_column(

            JSONB,

            nullable=False,

            default=dict,

        )
    )

    # =================================
    # WORKSPACE
    # =================================

    workspace_data: Mapped[dict] = (
        mapped_column(

            JSONB,

            nullable=False,

            default=dict,

        )
    )

    # =================================
    # EXECUTION
    # =================================

    execution_data: Mapped[dict] = (
        mapped_column(

            JSONB,

            nullable=False,

            default=dict,

        )
    )

    # =================================
    # CREATED AT
    # =================================

    created_at: Mapped[datetime] = (
        mapped_column(

            DateTime(
                timezone=True
            ),

            nullable=False,

            default=lambda: (
                datetime.now(
                    timezone.utc
                )
            ),

        )
    )

    # =================================
    # UPDATED AT
    # =================================

    updated_at: Mapped[datetime] = (
        mapped_column(

            DateTime(
                timezone=True
            ),

            nullable=False,

            default=lambda: (
                datetime.now(
                    timezone.utc
                )
            ),

            onupdate=lambda: (
                datetime.now(
                    timezone.utc
                )
            ),

        )
    )