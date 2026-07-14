from unittest.mock import MagicMock
import io
import json

from tests.integration.base import (
    IntegrationTestCase,
)


class ChatStreamFlowTests(
    IntegrationTestCase,
):

    # =====================================
    # COMPLETE STREAM FLOW
    # =====================================

    def test_chat_stream_lifecycle(
        self,
    ):

        # ==============================
        # CREATE SESSION
        # ==============================

        session = self.create_session()

        session_id = session[
            "session_id"
        ]

        # ==============================
        # MOCK DOCUMENT INGESTION
        # ==============================

        self.start_patch(

            "app.api.routes.routes_upload.classify_file",

            "pdf",

        )

        self.start_patch(

            "app.api.routes.routes_upload.ingest_pdf",

            {

                "pages": 2,

                "chunks": 4,

                "full_text":
                    "Dummy content",

                "pages_data": [

                    {

                        "page": 1,

                        "text":
                            "Artificial Intelligence",

                    }

                ],

            },

        )

        # ==============================
        # MOCK RESEARCH PIPELINE
        # ==============================

        fake_context = MagicMock()

        fake_context.session_id = session_id
        fake_context.provider = "mock-provider"
        fake_context.model = "mock-model"
        fake_context.intent = "document"
        fake_context.analysis = ""
        fake_context.response = None

        fake_stream = [

            "Ini ",

            "adalah ",

            "jawaban.",

        ]

        self.start_patch(

            "app.api.routes.routes_chat_stream.research_analysis",

            (

                fake_context,

                fake_stream,

            ),

        )

        # ==============================
        # MOCK SERIALIZER
        # ==============================

        self.start_patch(

            "app.api.routes.routes_chat_stream.serialize_research_context",

            {

                "mode": "document",

                "provider": "mock-provider",

            },

        )

        # ==============================
        # MOCK PERSISTENCE
        # ==============================

        self.start_patch(

            "app.api.routes.routes_chat_stream.persist_assistant_response",

            "Ini adalah jawaban.",

        )

        self.start_patch(

            "app.api.routes.routes_chat_stream.persist_execution_snapshot",

            {},

        )

        # ==============================
        # UPLOAD DOCUMENT
        # ==============================

        upload = self.client.post(

            "/upload-pdf",

            files={

                "file": (

                    "paper.pdf",

                    io.BytesIO(
                        b"pdf"
                    ),

                    "application/pdf",

                ),

            },

            data={

                "session_id":
                    session_id,

            },

        )

        self.assertEqual(
            upload.status_code,
            200,
        )

        document_id = upload.json()[
            "document_id"
        ]

        # ==============================
        # CHAT STREAM
        # ==============================

        response = self.client.post(

            "/chat-stream",

            json={

                "session_id":
                    session_id,

                "message":
                    "Jelaskan isi dokumen",

                "active_document_ids": [

                    document_id,

                ],

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        events = []

        for line in response.text.splitlines():

            if line.strip():

                events.append(
                    json.loads(line)
                )

        event_types = [

            event["type"]

            for event in events

        ]

        # ==============================
        # VERIFY EVENTS
        # ==============================

        self.assertIn(
            "start",
            event_types,
        )

        self.assertIn(
            "metadata",
            event_types,
        )

        self.assertIn(
            "context",
            event_types,
        )

        self.assertIn(
            "token",
            event_types,
        )

        self.assertIn(
            "context_final",
            event_types,
        )

        self.assertIn(
            "end",
            event_types,
        )

        # ==============================
        # VERIFY TOKEN OUTPUT
        # ==============================

        tokens = [

            event["data"]

            for event in events

            if event["type"] == "token"

        ]

        self.assertEqual(

            "".join(tokens),

            "Ini adalah jawaban.",

        )

        # ==============================
        # VERIFY END
        # ==============================

        end = [

            event

            for event in events

            if event["type"] == "end"

        ][0]

        self.assertEqual(

            end["data"]["status"],

            "completed",

        )