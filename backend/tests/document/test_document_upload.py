import io
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.routes_upload import router


app = FastAPI()

app.include_router(router)

client = TestClient(app)


class DocumentUploadTests(
    unittest.TestCase,
):

    def upload_file(
        self,
        session_id="session-1",
        filename="paper.pdf",
    ):

        return client.post(

            "/upload-pdf",

            data={
                "session_id": session_id,
            },

            files={
                "file": (
                    filename,
                    io.BytesIO(
                        b"fake pdf"
                    ),
                    "application/pdf",
                )
            },

        )

    @patch(
        "app.api.routes.routes_upload.ingest_pdf"
    )
    @patch(
        "app.api.routes.routes_upload.classify_file"
    )
    @patch(
        "app.api.routes.routes_upload.session_manager"
    )
    def test_upload_success(
        self,
        mock_manager,
        mock_classifier,
        mock_ingest,
    ):

        session = MagicMock()

        mock_manager.get.return_value = (
            session
        )

        mock_manager.save.return_value = (
            True
        )

        mock_classifier.return_value = (
            "pdf"
        )

        mock_ingest.return_value = {

            "pages": 12,

            "chunks": 45,

            "full_text": "content",

            "pages_data": [],

        }

        response = self.upload_file()

        self.assertEqual(
            response.status_code,
            200,
        )

        body = response.json()

        self.assertEqual(
            body["status"],
            "success",
        )

        self.assertEqual(
            body["filename"],
            "paper.pdf",
        )

        self.assertEqual(
            body["pages"],
            12,
        )

        self.assertEqual(
            body["chunks"],
            45,
        )

        session.documents.add_document.assert_called_once()

        mock_manager.save.assert_called_once()

    @patch(
        "app.api.routes.routes_upload.session_manager"
    )
    def test_upload_unknown_session(
        self,
        mock_manager,
    ):

        mock_manager.get.return_value = (
            None
        )

        response = self.upload_file()

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertEqual(

            response.json()["detail"],

            "Session not found",

        )

    @patch(
        "app.api.routes.routes_upload.ingest_pdf"
    )
    @patch(
        "app.api.routes.routes_upload.classify_file"
    )
    @patch(
        "app.api.routes.routes_upload.session_manager"
    )
    def test_upload_persistence_failure(
        self,
        mock_manager,
        mock_classifier,
        mock_ingest,
    ):

        session = MagicMock()

        mock_manager.get.return_value = (
            session
        )

        mock_manager.save.return_value = (
            False
        )

        mock_classifier.return_value = (
            "pdf"
        )

        mock_ingest.return_value = {

            "pages": 2,

            "chunks": 5,

            "full_text": "",

            "pages_data": [],

        }

        response = self.upload_file()

        self.assertEqual(
            response.status_code,
            500,
        )

        self.assertEqual(

            response.json()["detail"],

            "Document was ingested but session persistence failed",

        )

    @patch(
        "app.api.routes.routes_upload.ingest_pdf"
    )
    @patch(
        "app.api.routes.routes_upload.classify_file"
    )
    @patch(
        "app.api.routes.routes_upload.session_manager"
    )
    def test_document_added_to_session(
        self,
        mock_manager,
        mock_classifier,
        mock_ingest,
    ):

        session = MagicMock()

        mock_manager.get.return_value = (
            session
        )

        mock_manager.save.return_value = (
            True
        )

        mock_classifier.return_value = (
            "pdf"
        )

        mock_ingest.return_value = {

            "pages": 1,

            "chunks": 1,

            "full_text": "hello",

            "pages_data": [],

        }

        self.upload_file()

        self.assertEqual(

            session.documents.add_document.call_count,

            1,

        )

    @patch(
        "app.api.routes.routes_upload.ingest_pdf"
    )
    @patch(
        "app.api.routes.routes_upload.classify_file"
    )
    @patch(
        "app.api.routes.routes_upload.session_manager"
    )
    def test_ingest_receives_correct_session(
        self,
        mock_manager,
        mock_classifier,
        mock_ingest,
    ):

        session = MagicMock()

        session.session_id = "session-xyz"

        mock_manager.get.return_value = (
            session
        )

        mock_manager.save.return_value = (
            True
        )

        mock_classifier.return_value = (
            "pdf"
        )

        mock_ingest.return_value = {

            "pages": 1,

            "chunks": 2,

            "full_text": "",

            "pages_data": [],

        }

        self.upload_file(
            session_id="session-xyz"
        )

        kwargs = mock_ingest.call_args.kwargs

        self.assertEqual(

            kwargs["session_id"],

            "session-xyz",

        )

    @patch(
        "app.api.routes.routes_upload.ingest_pdf"
    )
    @patch(
        "app.api.routes.routes_upload.classify_file"
    )
    @patch(
        "app.api.routes.routes_upload.session_manager"
    )
    def test_classifier_receives_filename(
        self,
        mock_manager,
        mock_classifier,
        mock_ingest,
    ):

        session = MagicMock()

        mock_manager.get.return_value = (
            session
        )

        mock_manager.save.return_value = (
            True
        )

        mock_classifier.return_value = (
            "pdf"
        )

        mock_ingest.return_value = {

            "pages": 1,

            "chunks": 1,

            "full_text": "",

            "pages_data": [],

        }

        self.upload_file(
            filename="tesis.pdf"
        )

        mock_classifier.assert_called_once_with(
            "tesis.pdf"
        )