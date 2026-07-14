from copy import deepcopy

from app.services.research.session.models import (
    WorkspaceSession,
)


# =====================================
# FAKE SESSION REPOSITORY
# =====================================

class FakeSessionRepository:

    def __init__(
        self,
    ):

        self._storage: dict[
            str,
            WorkspaceSession,
        ] = {}

    # =================================
    # SAVE
    # =================================

    def save(
        self,
        session: WorkspaceSession,
    ) -> None:

        self._storage[
            session.session_id
        ] = deepcopy(session)

    # =================================
    # GET
    # =================================

    def get(
        self,
        session_id: str,
    ) -> WorkspaceSession | None:

        session = self._storage.get(
            session_id
        )

        if session is None:

            return None

        return deepcopy(
            session
        )

    # =================================
    # EXISTS
    # =================================

    def exists(
        self,
        session_id: str,
    ) -> bool:

        return (
            session_id
            in self._storage
        )

    # =================================
    # DELETE
    # =================================

    def delete(
        self,
        session_id: str,
    ) -> bool:

        return (

            self._storage.pop(
                session_id,
                None,
            )

            is not None

        )

    # =================================
    # CLEAR
    # =================================

    def clear(
        self,
    ):

        self._storage.clear()

    # =================================
    # COUNT
    # =================================

    def count(
        self,
    ) -> int:

        return len(
            self._storage
        )

    # =================================
    # LIST IDS
    # =================================

    def list_ids(
        self,
    ) -> list[str]:

        return list(
            self._storage.keys()
        )