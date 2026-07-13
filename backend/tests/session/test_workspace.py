import unittest

from app.services.research.session.models import (
    ConversationSession,
    DocumentSession,
    ExecutionSession,
    WorkspaceSession,
    WorkspaceState,
)


class WorkspaceSessionTests(
    unittest.TestCase,
):

    def setUp(
        self,
    ):

        self.workspace = WorkspaceSession(

            session_id="workspace-test",

            conversation=ConversationSession(),

            documents=DocumentSession(),

            workspace=WorkspaceState(),

            execution=ExecutionSession(),

        )

    # =====================================
    # CREATE
    # =====================================

    def test_workspace_has_expected_components(
        self,
    ):

        self.assertEqual(
            self.workspace.session_id,
            "workspace-test",
        )

        self.assertIsInstance(
            self.workspace.conversation,
            ConversationSession,
        )

        self.assertIsInstance(
            self.workspace.documents,
            DocumentSession,
        )

        self.assertIsInstance(
            self.workspace.workspace,
            WorkspaceState,
        )

        self.assertIsInstance(
            self.workspace.execution,
            ExecutionSession,
        )

    # =====================================
    # RESET
    # =====================================

    def test_reset_clears_conversation(
        self,
    ):

        self.workspace.conversation.append(

            role="user",

            content="hello",

        )

        self.workspace.reset()

        self.assertEqual(

            self.workspace.conversation.total_messages(),

            0,

        )

    def test_reset_clears_execution(
        self,
    ):

        self.workspace.execution.response = (
            "analysis"
        )

        self.workspace.reset()

        self.assertEqual(

            self.workspace.execution.response,

            "",

        )

    def test_reset_clears_workspace_state(
        self,
    ):

        self.workspace.workspace.last_search = (
            "artificial intelligence"
        )

        self.workspace.reset()

        self.assertEqual(

            self.workspace.workspace.last_search,

            "",

        )

    def test_reset_clears_documents(
        self,
    ):

        self.workspace.documents.documents[
            "doc-1"
        ] = object()

        self.workspace.reset()

        self.assertEqual(

            len(
                self.workspace.documents.documents
            ),

            0,

        )

    def test_reset_preserves_session_id(
        self,
    ):

        self.workspace.reset()

        self.assertEqual(

            self.workspace.session_id,

            "workspace-test",

        )

    # =====================================
    # SERIALIZATION
    # =====================================

    def test_to_dict_contains_all_sections(
        self,
    ):

        payload = (
            self.workspace.to_dict()
        )

        self.assertEqual(

            payload["session_id"],

            "workspace-test",

        )

        self.assertIn(
            "conversation",
            payload,
        )

        self.assertIn(
            "documents",
            payload,
        )

        self.assertIn(
            "workspace",
            payload,
        )

        self.assertIn(
            "execution",
            payload,
        )

    def test_to_dict_returns_dictionary(
        self,
    ):

        payload = (
            self.workspace.to_dict()
        )

        self.assertIsInstance(
            payload,
            dict,
        )


if __name__ == "__main__":
    unittest.main()