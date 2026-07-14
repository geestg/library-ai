import io

from tests.integration.base import (
    IntegrationTestCase,
)


class UploadFlowTests(
    IntegrationTestCase,
):

    # =====================================
    # SESSION -> UPLOAD -> LIST
    # =====================================

    def test_upload_document_updates_session(
        self,
    ):

        session = self.create_session()

        session_id = session[
            "session_id"
        ]

        self.start_patch(

            "app.api.routes.routes_upload.classify_file",

            "pdf",

        )

        self.start_patch(

            "app.api.routes.routes_upload.ingest_pdf",

            {

                "pages": 5,

                "chunks": 20,

                "full_text": "Dummy PDF",

                "pages_data": [

                    {

                        "page": 1,

                        "text": "Dummy",

                    }

                ],

            },

        )

        response = self.client.post(

            "/upload-pdf",

            files={

                "file": (

                    "paper.pdf",

                    io.BytesIO(
                        b"dummy pdf"
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
            response.status_code,
            200,
        )

        payload = response.json()

        self.assertEqual(

            payload["filename"],

            "paper.pdf",

        )

        self.assertEqual(

            payload["pages"],

            5,

        )

        self.assertEqual(

            payload["chunks"],

            20,

        )

        workspace = (

            self.session_manager.get(
                session_id
            )

        )

        self.assertIsNotNone(
            workspace
        )

        self.assertEqual(

            workspace.documents.count(),

            1,

        )

    # =====================================
    # MULTIPLE DOCUMENTS
    # =====================================

    def test_upload_multiple_documents(
        self,
    ):

        session = self.create_session()

        session_id = session[
            "session_id"
        ]

        self.start_patch(

            "app.api.routes.routes_upload.classify_file",

            "pdf",

        )

        self.start_patch(

            "app.api.routes.routes_upload.ingest_pdf",

            {

                "pages": 1,

                "chunks": 3,

                "full_text": "Dummy",

                "pages_data": [],

            },

        )

        for index in range(2):

            response = self.client.post(

                "/upload-pdf",

                files={

                    "file": (

                        f"paper_{index}.pdf",

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

                response.status_code,

                200,

            )

        workspace = (

            self.session_manager.get(
                session_id
            )

        )

        self.assertEqual(

            workspace.documents.count(),

            2,

        )

    # =====================================
    # LIST DOCUMENTS
    # =====================================

    def test_list_uploaded_documents(
        self,
    ):

        session = self.create_session()

        session_id = session[
            "session_id"
        ]

        self.start_patch(

            "app.api.routes.routes_upload.classify_file",

            "pdf",

        )

        self.start_patch(

            "app.api.routes.routes_upload.ingest_pdf",

            {

                "pages": 2,

                "chunks": 5,

                "full_text": "",

                "pages_data": [],

            },

        )

        self.client.post(

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

        listing = self.client.get(

            f"/session/{session_id}/documents"

        )

        self.assertEqual(

            listing.status_code,

            200,

        )

        payload = listing.json()

        self.assertEqual(

            payload["total_documents"],

            1,

        )

        document = payload[
            "documents"
        ][0]

        self.assertEqual(

            document["filename"],

            "paper.pdf",

        )

        self.assertEqual(

            document["pages"],

            2,

        )

        self.assertEqual(

            document["chunks"],

            5,

        )

    # =====================================
    # DELETE DOCUMENT
    # =====================================

    def test_delete_uploaded_document(
        self,
    ):

        session = self.create_session()

        session_id = session[
            "session_id"
        ]

        self.start_patch(

            "app.api.routes.routes_upload.classify_file",

            "pdf",

        )

        self.start_patch(

            "app.api.routes.routes_upload.ingest_pdf",

            {

                "pages": 1,

                "chunks": 1,

                "full_text": "",

                "pages_data": [],

            },

        )

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

        document_id = upload.json()[
            "document_id"
        ]

        deleted = self.client.delete(

            f"/session/{session_id}"

            f"/documents/{document_id}"

        )

        self.assertEqual(

            deleted.status_code,

            200,

        )

        workspace = (

            self.session_manager.get(
                session_id
            )

        )

        self.assertEqual(

            workspace.documents.count(),

            0,

        )