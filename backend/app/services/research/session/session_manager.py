from threading import RLock

from uuid import uuid4

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
            else str(uuid4())
        )

        if not resolved_session_id:
            resolved_session_id = str(
                uuid4()
            )

        with self._lock:

            existing_session = (
                self._sessions.get(
                    resolved_session_id
                )
            )

            if existing_session is not None:
                return existing_session

            session = WorkspaceSession(
                session_id=resolved_session_id,
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

        with self._lock:
            return self._sessions.get(
                session_id
            )

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
                with self._lock:
                    existing_session = (
                        self._sessions.get(
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
    # EXISTS
    # =====================================
    def exists(
        self,
        session_id: str,
    ) -> bool:

        if not session_id:
            return False

        with self._lock:
            return (
                session_id
                in self._sessions
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

        with self._lock:
            return (
                self._sessions.pop(
                    session_id,
                    None,
                )
                is not None
            )

    # =====================================
    # RESET SESSION
    # =====================================
    def reset(
        self,
        session_id: str,
    ) -> bool:

        with self._lock:

            session = self._sessions.get(
                session_id
            )

            if session is None:
                return False

            session.reset()
            return True

    # =====================================
    # LIST SESSION IDS
    # =====================================
    def list_session_ids(self) -> list[str]:
        with self._lock:
            return list(
                self._sessions.keys()
            )

    # =====================================
    # COUNT
    # =====================================
    def count(self) -> int:
        with self._lock:
            return len(
                self._sessions
            )

    # =====================================
    # LIST SESSIONS SUMMARY (FOR UI HISTORY)
    # =====================================
    def list_sessions_summary(self) -> list[dict]:
        with self._lock:
            summaries = []
            for s_id, session in self._sessions.items():
                messages = getattr(session.conversation, "messages", [])
                first_user_msg = ""
                for msg in messages:    
                    role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", "")
                    content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", "")
                    if role == "user" and content:
                        first_user_msg = str(content).strip()
                        break
                title = first_user_msg[:30] + ("..." if len(first_user_msg) > 30 else "") if first_user_msg else "Percakapan Baru"
                summaries.append({
                    "session_id": s_id,
                    "title": title,
                    "message_count": len(messages),
                    "created_at": getattr(session, "created_at", None)
                })
            return summaries

    # =====================================
    # CLEAR ALL
    # ====================================
    def clear(self):
        with self._lock:
            self._sessions.clear()

# =====================================
# SHARED SESSION MANAGER
# =====================================
session_manager = SessionManager()