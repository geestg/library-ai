import io

from tests.integration.base import (
    IntegrationTestCase,
)


class DocumentFlowTests(
    IntegrationTestCase,
):

    # =====================================
    # DOCUMENT LIFECYCLE
    # =====================================

    def test_document_chat_lifecycle(
        self,
    ):

        # =================================
        # CREATE SESSION
        # =================================

        session = self.create_session()

        session_id = session[
            "session_id"
        ]

        # =================================
        # MOCK UPLOAD DEPENDENCIES
        # =================================

        self.start_patch(

            "app.api.routes.routes_upload.classify_file",

            "pdf",

        )

        self.start_patch(

            "app.api.routes.routes_upload.ingest_pdf",

            {

                "pages": 4,

                "chunks": 12,

                "full_text":
                    "Dummy document content",

                "pages_data": [

                    {

                        "page": 1,

                        "text":
                            "Artificial Intelligence"

                    },

                    {

                        "page": 2,

                        "text":
                            "Machine Learning"

                    },

                ],

            },

        )

        # =================================
        # MOCK DOCUMENT CHAT
        # =================================

        self.start_patch(

            "app.api.routes.routes_document.detect_document_intent",

            "question",

        )

        self.start_patch(

            "app.api.routes.routes_document.retrieve_relevant_chunks",

            [

                {

                    "page": 1,

                    "text":
                        "Artificial Intelligence",

                }

            ],

        )

        self.start_patch(

            "app.api.routes.routes_document.LLMTask.execute",

            "Mock LLM Response",

        )

        # =================================
        # UPLOAD
        # =================================

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

        upload_payload = (
            upload.json()
        )

        document_id = upload_payload[
            "document_id"
        ]

        # =================================
        # VERIFY LIST
        # =================================

        listing = self.client.get(

            f"/session/{session_id}/documents"

        )

        self.assertEqual(
            listing.status_code,
            200,
        )

        payload = listing.json()

        self.assertEqual(

            payload[
                "total_documents"
            ],

            1,

        )

        self.assertEqual(

            payload[
                "documents"
            ][0][
                "document_id"
            ],

            document_id,

        )

        # =================================
        # DOCUMENT CHAT
        # =================================

        chat = self.client.post(

            "/document/chat",

            json={

                "session_id":
                    session_id,

                "document_id":
                    document_id,

                "question":
                    "Jelaskan isi dokumen",

            },

        )

        self.assertEqual(
            chat.status_code,
            200,
        )

        chat_payload = (
            chat.json()
        )

        self.assertEqual(

            chat_payload[
                "answer"
            ],

            "Mock LLM Response",

        )

        self.assertEqual(

            chat_payload[
                "intent"
            ],

            "question",

        )

        self.assertEqual(

            chat_payload[
                "retrieved_chunks"
            ],

            1,

        )

        # =================================
        # DELETE DOCUMENT
        # =================================

        deleted = self.client.delete(

            f"/session/{session_id}"

            f"/documents/{document_id}"

        )

        self.assertEqual(
            deleted.status_code,
            200,
        )

        # =================================
        # VERIFY EMPTY
        # =================================

        listing = self.client.get(

            f"/session/{session_id}/documents"

        )

        self.assertEqual(
            listing.status_code,
            200,
        )

        payload = listing.json()

        self.assertEqual(

            payload[
                "total_documents"
            ],

            0,

        )

    # =====================================
    # DOCUMENT CHAT UNKNOWN DOCUMENT
    # =====================================

    def test_document_chat_unknown_document(
        self,
    ):

        session = self.create_session()

        session_id = session[
            "session_id"
        ]

        response = self.client.post(

            "/document/chat",

            json={

                "session_id":
                    session_id,

                "document_id":
                    "missing",

                "question":
                    "Halo",

            },

        )

        self.assertEqual(
            response.status_code,
            404,
        )

    # =====================================
    # DOCUMENT CHAT UNKNOWN SESSION
    # =====================================

    def test_document_chat_unknown_session(
        self,
    ):

        response = self.client.post(

            "/document/chat",

            json={

                "session_id":
                    "missing",

                "document_id":
                    "missing",

                "question":
                    "Halo",

            },

        )

        self.assertEqual(
            response.status_code,
            404,
        )