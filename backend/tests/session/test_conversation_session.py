import unittest

from app.services.research.session.models.conversation_session import (
    ConversationMessage,
    ConversationSession,
    MAX_HISTORY,
)


class ConversationSessionTests(
    unittest.TestCase,
):

    def setUp(
        self,
    ):

        self.session = (
            ConversationSession()
        )

    # =====================================
    # APPEND
    # =====================================

    def test_append_adds_message(
        self,
    ):

        self.session.append(
            role="user",
            content="Hello",
        )

        self.assertEqual(
            self.session.total_messages(),
            1,
        )

        message = (
            self.session.last_message()
        )

        self.assertEqual(
            message.role,
            "user",
        )

        self.assertEqual(
            message.content,
            "Hello",
        )

    # =====================================
    # LEGACY WRAPPER
    # =====================================

    def test_add_message_uses_append(
        self,
    ):

        self.session.add_message(
            role="assistant",
            content="Hi",
        )

        self.assertEqual(
            self.session.total_messages(),
            1,
        )

        self.assertEqual(
            self.session.last_message().role,
            "assistant",
        )

    # =====================================
    # LAST MESSAGE
    # =====================================

    def test_last_message_returns_none_when_empty(
        self,
    ):

        self.assertIsNone(
            self.session.last_message()
        )

    def test_last_message_returns_latest(
        self,
    ):

        self.session.append(
            "user",
            "A",
        )

        self.session.append(
            "assistant",
            "B",
        )

        message = (
            self.session.last_message()
        )

        self.assertEqual(
            message.content,
            "B",
        )

    # =====================================
    # LAST USER
    # =====================================

    def test_last_user_message_returns_latest_user(
        self,
    ):

        self.session.append(
            "user",
            "first",
        )

        self.session.append(
            "assistant",
            "reply",
        )

        self.session.append(
            "user",
            "second",
        )

        message = (
            self.session.last_user_message()
        )

        self.assertEqual(
            message.content,
            "second",
        )

    def test_last_user_message_returns_none(
        self,
    ):

        self.session.append(
            "assistant",
            "reply",
        )

        self.assertIsNone(
            self.session.last_user_message()
        )

    # =====================================
    # LAST ASSISTANT
    # =====================================

    def test_last_assistant_message_returns_latest(
        self,
    ):

        self.session.append(
            "assistant",
            "one",
        )

        self.session.append(
            "user",
            "question",
        )

        self.session.append(
            "assistant",
            "two",
        )

        message = (
            self.session.last_assistant_message()
        )

        self.assertEqual(
            message.content,
            "two",
        )

    def test_last_assistant_message_returns_none(
        self,
    ):

        self.session.append(
            "user",
            "question",
        )

        self.assertIsNone(
            self.session.last_assistant_message()
        )

    # =====================================
    # BUILD HISTORY
    # =====================================

    def test_build_history_empty_returns_empty_string(
        self,
    ):

        self.assertEqual(
            self.session.build_history(),
            "",
        )

    def test_build_history_formats_messages(
        self,
    ):

        self.session.append(
            "user",
            "Hello",
        )

        self.session.append(
            "assistant",
            "Hi",
        )

        self.assertEqual(

            self.session.build_history(),

            "user: Hello\nassistant: Hi",

        )

    # =====================================
    # RETENTION
    # =====================================

    def test_retains_only_max_history(
        self,
    ):

        for i in range(
            MAX_HISTORY + 5
        ):

            self.session.append(
                "user",
                str(i),
            )

        self.assertEqual(
            self.session.total_messages(),
            MAX_HISTORY,
        )

        self.assertEqual(
            self.session.messages[0].content,
            "5",
        )

    # =====================================
    # CLEAR
    # =====================================

    def test_clear_removes_messages(
        self,
    ):

        self.session.append(
            "user",
            "hello",
        )

        self.session.clear()

        self.assertEqual(
            self.session.total_messages(),
            0,
        )

        self.assertEqual(
            self.session.build_history(),
            "",
        )

    # =====================================
    # SERIALIZATION
    # =====================================

    def test_to_dict_contains_messages(
        self,
    ):

        self.session.append(
            "user",
            "Hello",
        )

        payload = (
            self.session.to_dict()
        )

        self.assertEqual(
            payload["total_messages"],
            1,
        )

        self.assertEqual(
            payload["messages"][0]["role"],
            "user",
        )

        self.assertEqual(
            payload["messages"][0]["content"],
            "Hello",
        )

    def test_to_dict_empty_session(
        self,
    ):

        payload = (
            self.session.to_dict()
        )

        self.assertEqual(
            payload,
            {
                "messages": [],
                "total_messages": 0,
            },
        )

    # =====================================
    # DOMAIN OBJECT
    # =====================================

    def test_messages_are_conversation_message_instances(
        self,
    ):

        self.session.append(
            "user",
            "hello",
        )

        self.assertIsInstance(
            self.session.messages[0],
            ConversationMessage,
        )


if __name__ == "__main__":
    unittest.main()