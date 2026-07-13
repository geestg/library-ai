import unittest

from unittest.mock import MagicMock

from app.services.research.research_engine import (
    extract_assistant_content,
    persist_assistant_response,
)

from app.services.research.session.session_manager import (
    SessionManager,
)


class AssistantResponseTests(
    unittest.TestCase,
):

    def setUp(
        self,
    ):

        repository = MagicMock()

        repository.get.return_value = None

        repository.save.return_value = None

        repository.exists.return_value = False

        repository.delete.return_value = True

        self.manager = (
            SessionManager(
                repository=repository,
            )
        )

        self.session = (
            self.manager.create(
                "assistant-response-test"
            )
        )

    # =====================================
    # extract_assistant_content()
    # =====================================

    def test_extract_analysis_first(
        self,
    ):

        response = {

            "analysis": "Analysis",

            "answer": "Answer",

            "comparison": "Comparison",

        }

        self.assertEqual(

            extract_assistant_content(
                response
            ),

            "Analysis",

        )

    def test_extract_answer_fallback(
        self,
    ):

        response = {

            "analysis": "",

            "answer": "Answer",

        }

        self.assertEqual(

            extract_assistant_content(
                response
            ),

            "Answer",

        )

    def test_extract_comparison_fallback(
        self,
    ):

        response = {

            "comparison": "Comparison",

        }

        self.assertEqual(

            extract_assistant_content(
                response
            ),

            "Comparison",

        )

    def test_extract_returns_empty_when_response_is_none(
        self,
    ):

        self.assertEqual(

            extract_assistant_content(
                None
            ),

            "",

        )

    def test_extract_returns_empty_when_response_is_invalid(
        self,
    ):

        self.assertEqual(

            extract_assistant_content(
                []
            ),

            "",

        )

    def test_extract_returns_empty_when_all_fields_empty(
        self,
    ):

        response = {

            "analysis": "",

            "answer": "   ",

            "comparison": None,

        }

        self.assertEqual(

            extract_assistant_content(
                response
            ),

            "",

        )

    # =====================================
    # persist_assistant_response()
    # =====================================

    def test_persist_appends_assistant_message(
        self,
    ):

        content = (
            persist_assistant_response(

                session=self.session,

                response={

                    "analysis": "Assistant Reply",

                },

            )
        )

        self.assertEqual(

            content,

            "Assistant Reply",

        )

        self.assertEqual(

            self.session.conversation.total_messages(),

            1,

        )

        message = (
            self.session.conversation.last_message()
        )

        self.assertIsNotNone(
            message
        )

        self.assertEqual(

            message.role,

            "assistant",

        )

        self.assertEqual(

            message.content,

            "Assistant Reply",

        )

    def test_persist_returns_empty_when_content_empty(
        self,
    ):

        content = (
            persist_assistant_response(

                session=self.session,

                response={

                    "analysis": "   ",

                },

            )
        )

        self.assertEqual(

            content,

            "",

        )

        self.assertEqual(

            self.session.conversation.total_messages(),

            0,

        )

    def test_persist_returns_empty_when_response_invalid(
        self,
    ):

        content = (
            persist_assistant_response(

                session=self.session,

                response=None,

            )
        )

        self.assertEqual(

            content,

            "",

        )

        self.assertEqual(

            self.session.conversation.total_messages(),

            0,

        )


if __name__ == "__main__":

    unittest.main()