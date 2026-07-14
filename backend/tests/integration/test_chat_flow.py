from app.services.prompts.models.prompt_request import (
    PromptRequest,
)

from tests.integration.base import (
    IntegrationTestCase,
)


class ChatFlowTests(
    IntegrationTestCase,
):

    # =====================================
    # CHAT PIPELINE
    # =====================================

    def test_chat_pipeline(
        self,
    ):

        # ==============================
        # ROUTER
        # ==============================

        self.start_patch(

            "app.api.routes.routes_chat.route_query",

            {

                "intent": "research",

                "provider": "mock-provider",

                "model": "mock-model",

            },

        )

        # ==============================
        # HYBRID SEARCH
        # ==============================

        self.start_patch(

            "app.api.routes.routes_chat.hybrid_search",

            [

                {

                    "payload": {

                        "text":
                            "Artificial Intelligence",

                        "source_file":
                            "paper.pdf",

                        "page":
                            1,

                        "chunk_index":
                            0,

                        "title":
                            "Paper",

                    },

                    "score":
                        0.98,

                }

            ],

        )

        # ==============================
        # RERANK
        # ==============================

        self.start_patch(

            "app.api.routes.routes_chat.rerank",

            [

                {

                    "payload": {

                        "text":
                            "Artificial Intelligence",

                        "source_file":
                            "paper.pdf",

                        "page":
                            1,

                        "chunk_index":
                            0,

                        "title":
                            "Paper",

                    },

                    "rerank_score":
                        0.99,

                }

            ],

        )

        # ==============================
        # CONTEXT
        # ==============================

        self.start_patch(

            "app.api.routes.routes_chat.build_citation_context",

            "Mock Context",

        )

        # ==============================
        # PROMPT REQUEST
        # ==============================

        fake_request = PromptRequest.answer(
            "Mock Prompt"
        )

        self.start_patch(

            "app.api.routes.routes_chat.PromptRegistry.build_request",

            fake_request,

        )

        # ==============================
        # LLM
        # ==============================

        self.start_patch(

            "app.api.routes.routes_chat.LLMTask.execute",

            "Mock Answer",

        )

        # ==============================
        # SOURCE MAP
        # ==============================

        self.start_patch(

            "app.api.routes.routes_chat.build_source_map",

            [

                {

                    "source_id": 1,

                    "page": 1,

                }

            ],

        )

        # ==============================
        # REQUEST
        # ==============================

        response = self.client.post(

            "/chat",

            json={

                "message":
                    "Apa itu AI?",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        payload = response.json()

        self.assertEqual(
            payload["status"],
            "success",
        )

        self.assertEqual(
            payload["intent"],
            "research",
        )

        self.assertEqual(
            payload["provider"],
            "mock-provider",
        )

        self.assertEqual(
            payload["model"],
            "mock-model",
        )

        self.assertEqual(
            payload["response"],
            "Mock Answer",
        )

        self.assertEqual(
            len(payload["citations"]),
            1,
        )

        self.assertEqual(
            len(payload["sources"]),
            1,
        )

    # =====================================
    # EMPTY SEARCH RESULT
    # =====================================

    def test_chat_with_no_documents(
        self,
    ):

        self.start_patch(

            "app.api.routes.routes_chat.route_query",

            {

                "intent": "research",

                "provider": "mock-provider",

                "model": "mock-model",

            },

        )

        self.start_patch(

            "app.api.routes.routes_chat.hybrid_search",

            [],

        )

        self.start_patch(

            "app.api.routes.routes_chat.rerank",

            [],

        )

        self.start_patch(

            "app.api.routes.routes_chat.build_citation_context",

            "",

        )

        # ==============================
        # PROMPT REQUEST
        # ==============================

        fake_request = PromptRequest.answer(
            "Mock Prompt"
        )

        self.start_patch(

            "app.api.routes.routes_chat.PromptRegistry.build_request",

            fake_request,

        )

        self.start_patch(

            "app.api.routes.routes_chat.LLMTask.execute",

            "Tidak ditemukan",

        )

        self.start_patch(

            "app.api.routes.routes_chat.build_source_map",

            [],

        )

        response = self.client.post(

            "/chat",

            json={

                "message":
                    "Halo",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        payload = response.json()

        self.assertEqual(
            payload["response"],
            "Tidak ditemukan",
        )

        self.assertEqual(
            payload["citations"],
            [],
        )

        self.assertEqual(
            payload["sources"],
            [],
        )