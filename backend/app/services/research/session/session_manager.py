from threading import RLock

from uuid import uuid4

from app.persistence.session.repository import (
    session_repository,
)

from app.services.research.session.models import (
    ConversationSession,
    DocumentSession,
    ExecutionSession,
    WorkspaceSession,
    WorkspaceState,
)


# =====================================
# SESSION MANAGER
# =====================================

class SessionManager:

    def __init__(self):

        self._sessions: dict[
            str,
            WorkspaceSession,
        ] = {}

        self._lock = RLock()

        self._repository = (
            session_repository
        )

    # =====================================
    # CREATE SESSION
    # =====================================

    def create(
        self,
        session_id: str | None = None,
    ) -> WorkspaceSession:

        resolved_session_id = (

            session_id.strip()

            if session_id

            else str(
                uuid4()
            )

        )

        if not resolved_session_id:

            resolved_session_id = str(
                uuid4()
            )

        # =================================
        # CHECK MEMORY
        # =================================

        with self._lock:

            existing_session = (
                self._sessions.get(
                    resolved_session_id
                )
            )

            if existing_session is not None:

                return existing_session

        # =================================
        # CHECK DATABASE
        # =================================

        persisted_session = (
            self._repository.get(
                resolved_session_id
            )
        )

        if persisted_session is not None:

            with self._lock:

                self._sessions[
                    resolved_session_id
                ] = persisted_session

            return persisted_session

        # =================================
        # CREATE DOMAIN SESSION
        # =================================

        session = WorkspaceSession(

            session_id=(
                resolved_session_id
            ),

            conversation=(
                ConversationSession()
            ),

            documents=(
                DocumentSession()
            ),

            workspace=(
                WorkspaceState()
            ),

            execution=(
                ExecutionSession()
            ),

        )

        # =================================
        # PERSIST
        # =================================

        self._repository.save(
            session
        )

        # =================================
        # CACHE
        # =================================

        with self._lock:

            self._sessions[
                resolved_session_id
            ] = session

        return session

    # =====================================
    # GET SESSION
    # =====================================

    def get(
        self,
        session_id: str,
    ) -> WorkspaceSession | None:

        if not session_id:

            return None

        # =================================
        # MEMORY CACHE
        # =================================

        with self._lock:

            session = (
                self._sessions.get(
                    session_id
                )
            )

            if session is not None:

                return session

        # =================================
        # DATABASE FALLBACK
        # =================================

        session = (
            self._repository.get(
                session_id
            )
        )

        if session is None:

            return None

        # =================================
        # HYDRATE MEMORY CACHE
        # =================================

        with self._lock:

            self._sessions[
                session_id
            ] = session

        return session

    # =====================================
    # GET OR CREATE SESSION
    # =====================================

    def get_or_create(
        self,
        session_id: str | None = None,
    ) -> WorkspaceSession:

        if session_id:

            normalized_session_id = (
                session_id.strip()
            )

            if normalized_session_id:

                existing_session = (
                    self.get(
                        normalized_session_id
                    )
                )

                if existing_session is not None:

                    return existing_session

                return self.create(
                    normalized_session_id
                )

        return self.create()

    # =====================================
    # SAVE SESSION
    # =====================================

    def save(
        self,
        session_id: str,
    ) -> bool:

        if not session_id:

            return False

        with self._lock:

            session = (
                self._sessions.get(
                    session_id
                )
            )

        if session is None:

            return False

        self._repository.save(
            session
        )

        return True

    # =====================================
    # EXISTS
    # =====================================

    def exists(
        self,
        session_id: str,
    ) -> bool:

        if not session_id:

            return False

        with self._lock:

            if (
                session_id
                in self._sessions
            ):

                return True

        return self._repository.exists(
            session_id
        )

    # =====================================
    # DELETE SESSION
    # =====================================

    def delete(
        self,
        session_id: str,
    ) -> bool:

        if not session_id:

            return False

        # =================================
        # REMOVE MEMORY CACHE
        # =================================

        with self._lock:

            removed_from_memory = (

                self._sessions.pop(
                    session_id,
                    None,
                )

                is not None

            )

        # =================================
        # REMOVE DATABASE
        # =================================

        removed_from_database = (
            self._repository.delete(
                session_id
            )
        )

        return (

            removed_from_memory

            or

            removed_from_database

        )

    # =====================================
    # RESET SESSION
    # =====================================

    def reset(
        self,
        session_id: str,
    ) -> bool:

        session = self.get(
            session_id
        )

        if session is None:

            return False

        session.reset()

        self._repository.save(
            session
        )

        return True

    # =====================================
    # LIST CACHED SESSION IDS
    # =====================================

    def list_session_ids(
        self,
    ) -> list[str]:

        with self._lock:

            return list(
                self._sessions.keys()
            )

    # =====================================
    # COUNT CACHED SESSIONS
    # =====================================

    def count(
        self,
    ) -> int:

        with self._lock:

            return len(
                self._sessions
            )

    # =====================================
    # CLEAR MEMORY CACHE
    # =====================================

    def clear(
        self,
    ):

        with self._lock:

            self._sessions.clear()


# =====================================
# SHARED SESSION MANAGER
# =====================================

session_manager = SessionManager()

