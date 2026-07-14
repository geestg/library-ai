from unittest.mock import MagicMock

from tests.integration.base import (
    IntegrationTestCase,
)


class ResearchFlowTests(
    IntegrationTestCase,
):

    # =====================================
    # COMPLETE RESEARCH FLOW
    # =====================================

    def test_research_pipeline(
        self,
    ):

        # ==============================
        # SESSION
        # ==============================

        session = self.create_session()

        session_id = session[
            "session_id"
        ]

        # ==============================
        # MOCK CONTEXT
        # ==============================

        fake_context = MagicMock()

        fake_context.session_id = (
            session_id
        )

        fake_context.intent = (
            "research"
        )

        fake_context.provider = (
            "mock-provider"
        )

        fake_context.model = (
            "mock-model"
        )

        fake_context.analysis = (
            "Mock Research Analysis"
        )

        fake_context.response = (
            None
        )

        # ==============================
        # MOCK RESEARCH ANALYSIS
        # ==============================

        self.start_patch(

            "app.api.routes.routes_chat.research_analysis",

            (

                fake_context,

                None,

            ),

        )

        # ==============================
        # MOCK SERIALIZER
        # ==============================

        self.start_patch(

            "app.api.routes.routes_chat.serialize_research_context",

            {

                "intent":
                    "research",

                "provider":
                    "mock-provider",

            },

        )

        # ==============================
        # MOCK PERSISTENCE
        # ==============================

        self.start_patch(

            "app.api.routes.routes_chat.persist_assistant_response",

            "Mock Research Analysis",

        )

        self.start_patch(

            "app.api.routes.routes_chat.persist_execution_snapshot",

            {},

        )

        # ==============================
        # CHAT
        # ==============================

        response = self.client.post(

            "/chat",

            json={

                "session_id":
                    session_id,

                "message":
                    "Apa itu Artificial Intelligence?",

                "active_document_ids":
                    [],

            },

        )

        self.assertEqual(

            response.status_code,

            200,

        )

        payload = response.json()

        self.assertIn(
            "analysis",
            payload,
        )

        self.assertEqual(

            payload[
                "analysis"
            ],

            "Mock Research Analysis",

        )

        self.assertEqual(

            payload[
                "intent"
            ],

            "research",

        )

        self.assertEqual(

            payload[
                "provider"
            ],

            "mock-provider",

        )

    # =====================================
    # SESSION PERSISTS
    # =====================================

    def test_research_creates_conversation(
        self,
    ):

        session = self.create_session()

        session_id = session[
            "session_id"
        ]

        fake_context = MagicMock()

        fake_context.session_id = (
            session_id
        )

        fake_context.intent = (
            "research"
        )

        fake_context.provider = (
            "mock-provider"
        )

        fake_context.model = (
            "mock-model"
        )

        fake_context.analysis = (
            "Analysis"
        )

        fake_context.response = None

        self.start_patch(

            "app.api.routes.routes_chat.research_analysis",

            (

                fake_context,

                None,

            ),

        )

        self.start_patch(

            "app.api.routes.routes_chat.serialize_research_context",

            {},

        )

        self.start_patch(

            "app.api.routes.routes_chat.persist_assistant_response",

            "Analysis",

        )

        self.start_patch(

            "app.api.routes.routes_chat.persist_execution_snapshot",

            {},

        )

        response = self.client.post(

            "/chat",

            json={

                "session_id":
                    session_id,

                "message":
                    "Hello",

                "active_document_ids":
                    [],

            },

        )

        self.assertEqual(

            response.status_code,

            200,

        )

        workspace = (

            self.session_manager.get(
                session_id
            )

        )

        self.assertIsNotNone(
            workspace
        )