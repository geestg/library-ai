from datetime import datetime

from sqlalchemy import (
    delete,
    select,
)

from app.database.connection import (
    database_session_factory,
)

from app.persistence.session.models import (
    WorkspaceSessionRecord,
)

from app.services.research.session.models import (
    ConversationMessage,
    ConversationSession,
    DocumentItem,
    DocumentSession,
    ExecutionSession,
    WorkspaceSession,
    WorkspaceState,
)


# =====================================
# SESSION REPOSITORY
# =====================================

class SessionRepository:

    # =================================
    # SAVE
    # =================================

    def save(
        self,
        session: WorkspaceSession,
    ) -> None:

        with database_session_factory() as database:

            record = database.get(
                WorkspaceSessionRecord,
                session.session_id,
            )

            conversation_data = (
                session.conversation.to_dict()
            )

            documents_data = (
                session.documents.to_dict()
            )

            workspace_data = (
                session.workspace.to_dict()
            )

            execution_data = (
                session.execution.to_dict()
            )

            if record is None:

                record = WorkspaceSessionRecord(

                    session_id=(
                        session.session_id
                    ),

                    conversation_data=(
                        conversation_data
                    ),

                    documents_data=(
                        documents_data
                    ),

                    workspace_data=(
                        workspace_data
                    ),

                    execution_data=(
                        execution_data
                    ),

                )

                database.add(
                    record
                )

            else:

                record.conversation_data = (
                    conversation_data
                )

                record.documents_data = (
                    documents_data
                )

                record.workspace_data = (
                    workspace_data
                )

                record.execution_data = (
                    execution_data
                )

            database.commit()

    # =================================
    # GET
    # =================================

    def get(
        self,
        session_id: str,
    ) -> WorkspaceSession | None:

        with database_session_factory() as database:

            record = database.get(
                WorkspaceSessionRecord,
                session_id,
            )

            if record is None:

                return None

            return self._to_domain(
                record
            )

    # =================================
    # EXISTS
    # =================================

    def exists(
        self,
        session_id: str,
    ) -> bool:

        with database_session_factory() as database:

            statement = (

                select(
                    WorkspaceSessionRecord.session_id
                )

                .where(

                    WorkspaceSessionRecord.session_id
                    == session_id

                )

                .limit(1)

            )

            return (

                database.execute(
                    statement
                ).scalar_one_or_none()

                is not None

            )

    # =================================
    # DELETE
    # =================================

    def delete(
        self,
        session_id: str,
    ) -> bool:

        with database_session_factory() as database:

            statement = (

                delete(
                    WorkspaceSessionRecord
                )

                .where(

                    WorkspaceSessionRecord.session_id
                    == session_id

                )

            )

            result = database.execute(
                statement
            )

            database.commit()

            return (
                result.rowcount > 0
            )

    # =================================
    # HYDRATE DOMAIN SESSION
    # =================================

    def _to_domain(
        self,
        record: WorkspaceSessionRecord,
    ) -> WorkspaceSession:

        return WorkspaceSession(

            session_id=(
                record.session_id
            ),

            conversation=(
                self._build_conversation(
                    record.conversation_data
                )
            ),

            documents=(
                self._build_documents(
                    record.documents_data
                )
            ),

            workspace=(
                self._build_workspace(
                    record.workspace_data
                )
            ),

            execution=(
                self._build_execution(
                    record.execution_data
                )
            ),

        )

    # =================================
    # BUILD CONVERSATION
    # =================================

    def _build_conversation(
        self,
        data: dict | None,
    ) -> ConversationSession:

        payload = (
            data
            if isinstance(
                data,
                dict,
            )
            else {}
        )

        messages = []

        for item in payload.get(
            "messages",
            [],
        ):

            if not isinstance(
                item,
                dict,
            ):

                continue

            role = item.get(
                "role",
                "",
            )

            content = item.get(
                "content",
                "",
            )

            messages.append(

                ConversationMessage(

                    role=role,

                    content=content,

                )

            )

        return ConversationSession(
            messages=messages
        )

    # =================================
    # BUILD DOCUMENTS
    # =================================

    def _build_documents(
        self,
        data: dict | None,
    ) -> DocumentSession:

        payload = (
            data
            if isinstance(
                data,
                dict,
            )
            else {}
        )

        document_session = (
            DocumentSession()
        )

        for item in payload.get(
            "documents",
            [],
        ):

            if not isinstance(
                item,
                dict,
            ):

                continue

            document_id = item.get(
                "document_id",
                "",
            )

            if not document_id:

                continue

            document = DocumentItem(

                document_id=(
                    document_id
                ),

                filename=(
                    item.get(
                        "filename",
                        "",
                    )
                ),

                file_type=(
                    item.get(
                        "file_type",
                        "",
                    )
                ),

                pages=(
                    item.get(
                        "pages",
                        0,
                    )
                ),

                chunks=(
                    item.get(
                        "chunks",
                        0,
                    )
                ),

                content=(
                    item.get(
                        "content",
                        "",
                    )
                ),

                pages_data=(
                    item.get(
                        "pages_data",
                        [],
                    )
                ),

            )

            document_session.add_document(
                document
            )

        return document_session

    # =================================
    # BUILD WORKSPACE
    # =================================

    def _build_workspace(
        self,
        data: dict | None,
    ) -> WorkspaceState:

        payload = (
            data
            if isinstance(
                data,
                dict,
            )
            else {}
        )

        return WorkspaceState(

            selected_citation=(
                payload.get(
                    "selected_citation"
                )
            ),

            selected_thesis=(
                payload.get(
                    "selected_thesis"
                )
            ),

            last_search=(
                payload.get(
                    "last_search",
                    "",
                )
            ),

            filters=(
                payload.get(
                    "filters",
                    {},
                )
            ),

            ui_state=(
                payload.get(
                    "ui_state",
                    {},
                )
            ),

        )

    # =================================
    # BUILD EXECUTION
    # =================================

    def _build_execution(
        self,
        data: dict | None,
    ) -> ExecutionSession:

        payload = (
            data
            if isinstance(
                data,
                dict,
            )
            else {}
        )

        updated_at = payload.get(
            "updated_at"
        )

        parsed_updated_at = None

        if isinstance(
            updated_at,
            str,
        ):

            try:

                parsed_updated_at = (
                    datetime.fromisoformat(
                        updated_at
                    )
                )

            except ValueError:

                parsed_updated_at = None

        return ExecutionSession(

            last_query=(
                payload.get(
                    "last_query",
                    "",
                )
            ),

            mode=(
                payload.get(
                    "mode",
                    "",
                )
            ),

            provider=(
                payload.get(
                    "provider",
                    "",
                )
            ),

            model=(
                payload.get(
                    "model",
                    "",
                )
            ),

            intent=(
                payload.get(
                    "intent",
                    "",
                )
            ),

            response=(
                payload.get(
                    "response",
                    "",
                )
            ),

            serialized_context=(
                payload.get(
                    "serialized_context",
                    {},
                )
            ),

            updated_at=(
                parsed_updated_at
            ),

        )


# =====================================
# SHARED SESSION REPOSITORY
# =====================================

session_repository = (
    SessionRepository()
)

