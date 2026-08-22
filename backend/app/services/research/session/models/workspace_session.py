from dataclasses import dataclass, field

from .conversation_session import (
    ConversationSession,
)

from .document_session import (
    DocumentSession,
)

from .execution_session import (
    ExecutionSession,
)

from .workspace_state import (
    WorkspaceState,
)


# =====================================
# WORKSPACE SESSION
# =====================================

@dataclass
class WorkspaceSession:

    # =================================
    # SESSION INFO
    # =================================

    session_id: str

    # =================================
    # SUB SESSIONS
    # =================================

    conversation: ConversationSession

    documents: DocumentSession

    workspace: WorkspaceState

    execution: ExecutionSession

    # Sticky Program Studi for this session (e.g. 'Informatika', 'Sistem Informasi')
    prodi: str = ""

    # Last intent detected for this session (e.g. 'thesis_idea', 'literature')
    # Used to maintain continuity for follow-up messages that lack clear keywords.
    last_intent: str = ""

    # Set of thesis titles already used as citations in this session.
    # Follow-up searches will deprioritize/exclude these to surface different papers.
    used_titles: set = field(default_factory=set)

    # Tracks the number of follow-up requests in this session.
    # Used as an offset multiplier to fetch different sets of documents on follow-ups.
    followup_count: int = 0

    # Cumulative list of all theses retrieved and used as citations in this session
    all_theses: list = field(default_factory=list)

    # =====================================
    # SERIALIZER
    # =====================================

    def to_dict(self):

        return {

            "session_id":
                self.session_id,

            "conversation":
                self.conversation.to_dict(),

            "documents":
                self.documents.to_dict(),

            "workspace":
                self.workspace.to_dict(),

            "execution":
                self.execution.to_dict(),

            "sources":
                self.all_theses,

            "citations":
                self.all_theses,

        }

    # =====================================
    # RESET CONVERSATION
    # =====================================

    def clear_conversation(self):

        self.conversation.clear()

    # =====================================
    # RESET DOCUMENTS
    # =====================================

    def clear_documents(self):

        self.documents.clear()

    # =====================================
    # RESET EXECUTION
    # =====================================

    def clear_execution(self):

        self.execution.clear()
        self.followup_count = 0
        self.used_titles.clear()
        self.all_theses.clear()

    # =====================================
    # RESET WORKSPACE
    # =====================================

    def clear_workspace(self):

        self.workspace.clear()

    # =====================================
    # RESET ALL
    # =====================================

    def reset(self):

        self.clear_conversation()

        self.clear_documents()

        self.clear_execution()

        self.clear_workspace()