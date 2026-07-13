import unittest
from unittest.mock import Mock
from unittest.mock import patch

from app.services.research.prompts.analysis_prompt_builder import (
    build_conversation_section,
    build_research_prompt,
)

from app.services.research.session import (
    session_manager,
)

from app.services.research.session.models.conversation_session import (
    ConversationSession,
    MAX_HISTORY,
)

from app.services.research.research_engine import (
    research_analysis,
)

from tests.helpers import (
    build_context,
)


# =====================================
# CONVERSATION PROMPT TESTS
# =====================================

class ConversationPromptTests(
    unittest.TestCase
):

    def test_empty_conversation_history_uses_explicit_fallback(
        self,
    ):

        context = build_context()

        section = (
            build_conversation_section(
                context
            )
        )

        self.assertEqual(

            section,

            "Belum ada percakapan sebelumnya.",

        )

    def test_existing_conversation_history_is_included_in_prompt(
        self,
    ):

        context = build_context(
            "lanjutkan analisis tersebut"
        )

        context.conversation_history = (

            "user: jelaskan artificial intelligence\n"
            "assistant: Artificial intelligence adalah "
            "bidang ilmu komputer."

        )

        prompt = (
            build_research_prompt(
                context
            )
        )

        self.assertIn(

            context.conversation_history,

            prompt,

        )

    def test_current_query_is_included_in_prompt(
        self,
    ):

        context = build_context(
            "apa research gap dari topik tersebut?"
        )

        context.conversation_history = (

            "user: analisis artificial intelligence\n"
            "assistant: Topik tersebut memiliki "
            "beberapa tren penelitian."

        )

        prompt = (
            build_research_prompt(
                context
            )
        )

        self.assertIn(

            context.query,

            prompt,

        )

    def test_previous_history_and_current_query_remain_separate(
        self,
    ):

        previous_query = (
            "jelaskan tren artificial intelligence"
        )

        current_query = (
            "apa research gap dari topik tersebut?"
        )

        context = build_context(
            current_query
        )

        context.conversation_history = (

            f"user: {previous_query}\n"
            "assistant: Tren penelitian berkembang "
            "pada beberapa pendekatan."

        )

        prompt = (
            build_research_prompt(
                context
            )
        )

        history_heading = (
            "RIWAYAT PERCAKAPAN"
        )

        current_query_heading = (
            "PERTANYAAN SAAT INI"
        )

        self.assertLess(

            prompt.index(history_heading),

            prompt.index(previous_query),

        )

        self.assertLess(

            prompt.index(previous_query),

            prompt.index(current_query_heading),

        )

        self.assertLess(

            prompt.index(current_query_heading),

            prompt.index(current_query),

        )


# =====================================
# CONVERSATION RETENTION TESTS
# =====================================

class ConversationRetentionTests(
    unittest.TestCase
):

    def setUp(
        self,
    ):

        self.conversation = (
            ConversationSession()
        )

    def test_conversation_retains_only_max_history_messages(
        self,
    ):

        total_messages = (
            MAX_HISTORY + 3
        )

        for index in range(total_messages):

            self.conversation.append(

                role="user",

                content=f"message-{index}",

            )

        self.assertEqual(

            self.conversation.total_messages(),

            MAX_HISTORY,

        )

    def test_conversation_discards_oldest_messages_when_limit_is_exceeded(
        self,
    ):

        total_messages = (
            MAX_HISTORY + 3
        )

        for index in range(total_messages):

            self.conversation.append(

                role="user",

                content=f"message-{index}",

            )

        retained = [

            message.content

            for message in self.conversation.messages

        ]

        expected = [

            f"message-{index}"

            for index in range(

                3,

                total_messages,

            )

        ]

        self.assertEqual(

            retained,

            expected,

        )

    def test_conversation_preserves_message_order_after_retention(
        self,
    ):

        total_messages = (
            MAX_HISTORY + 2
        )

        for index in range(total_messages):

            self.conversation.append(

                role=(

                    "user"

                    if index % 2 == 0

                    else "assistant"

                ),

                content=f"message-{index}",

            )

        retained = [

            (

                message.role,

                message.content,

            )

            for message in self.conversation.messages

        ]

        expected = [

            (

                "user"

                if index % 2 == 0

                else "assistant",

                f"message-{index}",

            )

            for index in range(

                2,

                total_messages,

            )

        ]

        self.assertEqual(

            retained,

            expected,

        )

    def test_build_history_uses_only_retained_messages(
        self,
    ):

        total_messages = (
            MAX_HISTORY + 2
        )

        for index in range(total_messages):

            self.conversation.append(

                role=(

                    "user"

                    if index % 2 == 0

                    else "assistant"

                ),

                content=f"message-{index}",

            )

        history = self.conversation.build_history()

        self.assertEqual(

            len(history.splitlines()),

            MAX_HISTORY,

        )

        self.assertNotIn(

            "message-0",

            history,

        )

        self.assertIn(

            f"message-{total_messages-1}",

            history,

        )


# =====================================
# CONVERSATION INTEGRITY TESTS
# =====================================

class ConversationIntegrityTests(
    unittest.TestCase
):

    def setUp(
        self,
    ):

        self.conversation = (
            ConversationSession()
        )

    def test_conversation_preserves_user_assistant_order(
        self,
    ):

        self.conversation.append(

            role="user",

            content="Pertanyaan pertama",

        )

        self.conversation.append(

            role="assistant",

            content="Jawaban pertama",

        )

        self.conversation.append(

            role="user",

            content="Pertanyaan kedua",

        )

        self.conversation.append(

            role="assistant",

            content="Jawaban kedua",

        )

        self.assertEqual(

            [

                (

                    m.role,

                    m.content,

                )

                for m in self.conversation.messages

            ],

            [

                (

                    "user",

                    "Pertanyaan pertama",

                ),

                (

                    "assistant",

                    "Jawaban pertama",

                ),

                (

                    "user",

                    "Pertanyaan kedua",

                ),

                (

                    "assistant",

                    "Jawaban kedua",

                ),

            ],

        )

    def test_last_user_message_returns_latest_user_message(
        self,
    ):

        self.conversation.append(

            role="user",

            content="A",

        )

        self.conversation.append(

            role="assistant",

            content="B",

        )

        self.conversation.append(

            role="user",

            content="C",

        )

        self.assertEqual(

            self.conversation.last_user_message().content,

            "C",

        )

    def test_last_assistant_message_returns_latest_assistant_message(
        self,
    ):

        self.conversation.append(

            role="user",

            content="A",

        )

        self.conversation.append(

            role="assistant",

            content="B",

        )

        self.conversation.append(

            role="assistant",

            content="C",

        )

        self.assertEqual(

            self.conversation.last_assistant_message().content,

            "C",

        )

    def test_conversation_serialization_preserves_message_contract(
        self,
    ):

        self.conversation.append(

            role="user",

            content="Analisis",

        )

        self.conversation.append(

            role="assistant",

            content="Jawaban",

        )

        serialized = (

            self.conversation.to_dict()

        )

        self.assertEqual(

            serialized["total_messages"],

            2,

        )


