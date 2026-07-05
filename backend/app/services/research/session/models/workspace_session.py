from dataclasses import dataclass

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