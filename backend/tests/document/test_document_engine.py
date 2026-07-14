import unittest
from unittest.mock import patch

from app.services.research.session.models import (
    DocumentItem,
    DocumentSession,
)


class FakeWorkspaceSession:

    def __init__(self):

        self.documents = DocumentSession()


class ResolveActiveDocumentsTests(
    unittest.TestCase,
):

    def build_document(
        self,
        document_id,
        filename=None,
    ):

        return DocumentItem(

            document_id=document_id,

            filename=filename or f"{document_id}.pdf",

            file_type="pdf",

            pages=10,

            chunks=20,

            content="content",

        )

    @patch(
        "app.services.research.engines.document_engine.session_manager"
    )
    def test_unknown_session_returns_empty_list(
        self,
        mock_manager,
    ):

        from app.services.research.engines.document_engine import (
            resolve_active_documents,
        )

        mock_manager.get.return_value = None

        documents = resolve_active_documents(

            session_id="missing",

            active_document_ids=[
                "doc-1",
            ],

        )

        self.assertEqual(
            documents,
            [],
        )

    @patch(
        "app.services.research.engines.document_engine.session_manager"
    )
    def test_empty_document_ids_returns_empty(
        self,
        mock_manager,
    ):

        from app.services.research.engines.document_engine import (
            resolve_active_documents,
        )

        session = FakeWorkspaceSession()

        mock_manager.get.return_value = session

        documents = resolve_active_documents(

            session_id="session",

            active_document_ids=[],

        )

        self.assertEqual(
            documents,
            [],
        )

    @patch(
        "app.services.research.engines.document_engine.session_manager"
    )
    def test_existing_document_is_returned(
        self,
        mock_manager,
    ):

        from app.services.research.engines.document_engine import (
            resolve_active_documents,
        )

        session = FakeWorkspaceSession()

        session.documents.add_document(

            self.build_document(
                "doc-1",
                "paper.pdf",
            )

        )

        mock_manager.get.return_value = session

        documents = resolve_active_documents(

            session_id="session",

            active_document_ids=[
                "doc-1",
            ],

        )

        self.assertEqual(
            len(documents),
            1,
        )

        self.assertEqual(

            documents[0]["document_id"],

            "doc-1",

        )

        self.assertEqual(

            documents[0]["filename"],

            "paper.pdf",

        )

    @patch(
        "app.services.research.engines.document_engine.session_manager"
    )
    def test_unknown_document_is_ignored(
        self,
        mock_manager,
    ):

        from app.services.research.engines.document_engine import (
            resolve_active_documents,
        )

        session = FakeWorkspaceSession()

        mock_manager.get.return_value = session

        documents = resolve_active_documents(

            session_id="session",

            active_document_ids=[
                "missing",
            ],

        )

        self.assertEqual(
            documents,
            [],
        )

    @patch(
        "app.services.research.engines.document_engine.session_manager"
    )
    def test_multiple_documents_preserve_order(
        self,
        mock_manager,
    ):

        from app.services.research.engines.document_engine import (
            resolve_active_documents,
        )

        session = FakeWorkspaceSession()

        session.documents.add_document(
            self.build_document("A")
        )

        session.documents.add_document(
            self.build_document("B")
        )

        session.documents.add_document(
            self.build_document("C")
        )

        mock_manager.get.return_value = session

        documents = resolve_active_documents(

            session_id="session",

            active_document_ids=[
                "A",
                "B",
                "C",
            ],

        )

        self.assertEqual(

            [

                d["document_id"]

                for d in documents

            ],

            [

                "A",
                "B",
                "C",

            ],

        )

    @patch(
        "app.services.research.engines.document_engine.session_manager"
    )
    def test_missing_documents_are_filtered(
        self,
        mock_manager,
    ):

        from app.services.research.engines.document_engine import (
            resolve_active_documents,
        )

        session = FakeWorkspaceSession()

        session.documents.add_document(
            self.build_document("A")
        )

        session.documents.add_document(
            self.build_document("C")
        )

        mock_manager.get.return_value = session

        documents = resolve_active_documents(

            session_id="session",

            active_document_ids=[
                "A",
                "B",
                "C",
            ],

        )

        self.assertEqual(
            len(documents),
            2,
        )

        self.assertEqual(

            [

                d["document_id"]

                for d in documents

            ],

            [

                "A",
                "C",
            ],

        )

    @patch(
        "app.services.research.engines.document_engine.session_manager"
    )
    def test_metadata_is_preserved(
        self,
        mock_manager,
    ):

        from app.services.research.engines.document_engine import (
            resolve_active_documents,
        )

        session = FakeWorkspaceSession()

        session.documents.add_document(

            DocumentItem(

                document_id="doc",

                filename="paper.pdf",

                file_type="pdf",

                pages=15,

                chunks=87,

            )

        )

        mock_manager.get.return_value = session

        document = resolve_active_documents(

            session_id="session",

            active_document_ids=[
                "doc",
            ],

        )[0]

        self.assertEqual(
            document["pages"],
            15,
        )

        self.assertEqual(
            document["chunks"],
            87,
        )

        self.assertEqual(
            document["file_type"],
            "pdf",
        )