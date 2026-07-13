import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.routes_session import router


app = FastAPI()

app.include_router(router)

client = TestClient(app)


class SessionRoutesTests(
    unittest.TestCase,
):

    @patch(
        "app.api.routes.routes_session.session_manager"
    )
    def test_create_session(
        self,
        mock_manager,
    ):

        session = MagicMock()

        session.to_dict.return_value = {

            "session_id": "session-1",

            "conversation": {},

            "documents": {},

            "workspace": {},

            "execution": {},

        }

        mock_manager.create.return_value = (
            session
        )

        response = client.post(
            "/session/create"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        body = response.json()

        self.assertEqual(
            body["session_id"],
            "session-1",
        )

        self.assertIn(
            "conversation",
            body,
        )

        self.assertIn(
            "documents",
            body,
        )

        self.assertIn(
            "workspace",
            body,
        )

        self.assertIn(
            "execution",
            body,
        )

    @patch(
        "app.api.routes.routes_session.session_manager"
    )
    def test_get_existing_session(
        self,
        mock_manager,
    ):

        session = MagicMock()

        session.to_dict.return_value = {

            "session_id": "abc",

        }

        mock_manager.get.return_value = (
            session
        )

        response = client.get(
            "/session/abc"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(

            response.json()["session_id"],

            "abc",

        )

    @patch(
        "app.api.routes.routes_session.session_manager"
    )
    def test_get_missing_session_returns_404(
        self,
        mock_manager,
    ):

        mock_manager.get.return_value = (
            None
        )

        response = client.get(
            "/session/missing"
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertEqual(

            response.json()["detail"],

            "Session not found.",

        )

    @patch(
        "app.api.routes.routes_session.session_manager"
    )
    def test_delete_existing_session(
        self,
        mock_manager,
    ):

        mock_manager.delete.return_value = (
            True
        )

        response = client.delete(
            "/session/session-1"
        )

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

            body["session_id"],

            "session-1",

        )

    @patch(
        "app.api.routes.routes_session.session_manager"
    )
    def test_delete_missing_session_returns_404(
        self,
        mock_manager,
    ):

        mock_manager.delete.return_value = (
            False
        )

        response = client.delete(
            "/session/missing"
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertEqual(

            response.json()["detail"],

            "Session not found.",

        )

    @patch(
        "app.api.routes.routes_session.session_manager"
    )
    def test_delete_document_success(
        self,
        mock_manager,
    ):

        session = MagicMock()

        session.documents.get_document.return_value = (
            object()
        )

        mock_manager.get.return_value = (
            session
        )

        mock_manager.save.return_value = (
            True
        )

        response = client.delete(
            "/session/session-1/documents/doc-1"
        )

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
            body["document_id"],
            "doc-1",
        )

        session.documents.remove_document.assert_called_once_with(
            "doc-1"
        )

    @patch(
        "app.api.routes.routes_session.session_manager"
    )
    def test_delete_document_unknown_session(
        self,
        mock_manager,
    ):

        mock_manager.get.return_value = (
            None
        )

        response = client.delete(
            "/session/session-1/documents/doc-1"
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertEqual(

            response.json()["detail"],

            "Session not found.",

        )

    @patch(
        "app.api.routes.routes_session.session_manager"
    )
    def test_delete_document_unknown_document(
        self,
        mock_manager,
    ):

        session = MagicMock()

        session.documents.get_document.return_value = (
            None
        )

        mock_manager.get.return_value = (
            session
        )

        response = client.delete(
            "/session/session-1/documents/doc-1"
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertEqual(

            response.json()["detail"],

            "Document not found.",

        )

    @patch(
        "app.api.routes.routes_session.session_manager"
    )
    def test_delete_document_persistence_failure(
        self,
        mock_manager,
    ):

        session = MagicMock()

        session.documents.get_document.return_value = (
            object()
        )

        mock_manager.get.return_value = (
            session
        )

        mock_manager.save.return_value = (
            False
        )

        response = client.delete(
            "/session/session-1/documents/doc-1"
        )

        self.assertEqual(
            response.status_code,
            500,
        )

        self.assertEqual(

            response.json()["detail"],

            "Document was removed but session persistence failed.",

        )