from app.services.research.session.models import (
    WorkspaceSession,
)


class FakeSessionRepository:

    def __init__(
        self,
    ):

        self.storage: dict[
            str,
            WorkspaceSession,
        ] = {}

    # =====================================
    # SAVE
    # =====================================

    def save(
        self,
        session: WorkspaceSession,
    ) -> None:

        self.storage[
            session.session_id
        ] = session

    # =====================================
    # GET
    # =====================================

    def get(
        self,
        session_id: str,
    ) -> WorkspaceSession | None:

        return self.storage.get(
            session_id
        )

    # =====================================
    # EXISTS
    # =====================================

    def exists(
        self,
        session_id: str,
    ) -> bool:

        return (
            session_id
            in self.storage
        )

    # =====================================
    # DELETE
    # =====================================

    def delete(
        self,
        session_id: str,
    ) -> bool:

        return (

            self.storage.pop(
                session_id,
                None,
            )

            is not None

        )