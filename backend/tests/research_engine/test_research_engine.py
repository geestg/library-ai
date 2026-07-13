import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from app.services.research.models.research_context import ResearchContext
from app.services.research.research_engine import research_analysis


class FakeConversation:

    def __init__(self):
        self.messages = []

    def append(self, role, content):
        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    def build_history(self):
        return "\n".join(
            f"{m['role']}: {m['content']}"
            for m in self.messages
        )


class FakeExecution:

    def __init__(self):
        self.updated = False
        self.context = None
        self.serialized_context = None
        self.response_content = None

    def update(
        self,
        context,
        serialized_context,
        response_content,
    ):
        self.updated = True
        self.context = context
        self.serialized_context = serialized_context
        self.response_content = response_content


class FakeSession:

    def __init__(self):
        self.session_id = "test-session"
        self.conversation = FakeConversation()
        self.execution = FakeExecution()


class ResearchEngineConversationTests(unittest.TestCase):

    @patch(
        "app.orchestration.task_router.route_query"
    )
    @patch(
        "app.services.research.research_engine.serialize_research_context"
    )
    @patch(
        "app.services.research.research_engine.ResearchPipelineBuilder.build"
    )
    @patch(
        "app.services.research.research_engine.session_manager"
    )
    def test_research_analysis_snapshots_history_before_current_user_message(
        self,
        mock_session_manager,
        mock_build,
        mock_serializer,
        mock_route,
    ):

        fake_session = FakeSession()

        fake_session.conversation.append(
            "user",
            "Old Question",
        )

        fake_session.conversation.append(
            "assistant",
            "Old Answer",
        )

        mock_session_manager.get_or_create.return_value = fake_session

        mock_route.return_value = {
            "intent": "analysis",
            "provider": "mock",
            "model": "mock",
        }

        mock_serializer.return_value = {
            "conversation": "serialized",
        }

        captured_context = {}

        executor = MagicMock()

        def fake_run():

            context = captured_context["context"]

            context.response = {
                "analysis": "Assistant Reply",
            }

        executor.run.side_effect = fake_run

        def fake_build(
            context,
            stream=False,
            progress_callback=None,
        ):

            captured_context["context"] = context

            return executor

        mock_build.side_effect = fake_build

        response = research_analysis(
            query="Current Question",
            session_id="test-session",
        )

        context = captured_context["context"]

        self.assertEqual(
            response["analysis"],
            "Assistant Reply",
        )

        self.assertEqual(
            context.conversation_history,
            "user: Old Question\nassistant: Old Answer",
        )

        self.assertEqual(
            fake_session.conversation.messages[0]["content"],
            "Old Question",
        )

        self.assertEqual(
            fake_session.conversation.messages[1]["content"],
            "Old Answer",
        )

        self.assertEqual(
            fake_session.conversation.messages[2]["content"],
            "Current Question",
        )

        self.assertEqual(
            fake_session.conversation.messages[3]["content"],
            "Assistant Reply",
        )

        self.assertTrue(
            fake_session.execution.updated
        )

        self.assertIsInstance(
            fake_session.execution.context,
            ResearchContext,
        )

        self.assertEqual(
            fake_session.execution.response_content,
            "Assistant Reply",
        )


if __name__ == "__main__":
    unittest.main()