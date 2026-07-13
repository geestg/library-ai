import unittest

from app.services.research.session.models import (
    DocumentItem,
    DocumentSession,
)


class DocumentSessionTests(
    unittest.TestCase,
):

    def build_document(
        self,
        document_id="doc-1",
        filename="paper.pdf",
    ):

        return DocumentItem(

            document_id=document_id,

            filename=filename,

            file_type="pdf",

            pages=12,

            chunks=45,

            content="example content",

            pages_data=[
                {
                    "page": 1,
                }
            ],

        )

    # =====================================
    # DEFAULT
    # =====================================

    def test_default_session_is_empty(
        self,
    ):

        session = DocumentSession()

        self.assertEqual(
            session.count(),
            0,
        )

        self.assertEqual(
            session.documents,
            {},
        )

    # =====================================
    # ADD
    # =====================================

    def test_add_document(
        self,
    ):

        session = DocumentSession()

        document = self.build_document()

        session.add_document(
            document
        )

        self.assertEqual(
            session.count(),
            1,
        )

        self.assertIs(

            session.get_document(
                "doc-1"
            ),

            document,

        )

    def test_add_duplicate_document_replaces_existing(
        self,
    ):

        session = DocumentSession()

        session.add_document(
            self.build_document(
                "doc-1",
                "old.pdf",
            )
        )

        replacement = self.build_document(
            "doc-1",
            "new.pdf",
        )

        session.add_document(
            replacement
        )

        self.assertEqual(
            session.count(),
            1,
        )

        self.assertEqual(

            session.get_document(
                "doc-1"
            ).filename,

            "new.pdf",

        )

    # =====================================
    # GET
    # =====================================

    def test_get_existing_document(
        self,
    ):

        session = DocumentSession()

        document = self.build_document()

        session.add_document(
            document
        )

        self.assertIs(

            session.get_document(
                "doc-1"
            ),

            document,

        )

    def test_get_missing_document_returns_none(
        self,
    ):

        session = DocumentSession()

        self.assertIsNone(

            session.get_document(
                "missing"
            )

        )

    # =====================================
    # REMOVE
    # =====================================

    def test_remove_existing_document(
        self,
    ):

        session = DocumentSession()

        session.add_document(
            self.build_document()
        )

        session.remove_document(
            "doc-1"
        )

        self.assertEqual(
            session.count(),
            0,
        )

    def test_remove_missing_document_is_safe(
        self,
    ):

        session = DocumentSession()

        session.remove_document(
            "unknown"
        )

        self.assertEqual(
            session.count(),
            0,
        )

    def test_remove_one_document_preserves_others(
        self,
    ):

        session = DocumentSession()

        session.add_document(
            self.build_document(
                "doc-1"
            )
        )

        session.add_document(
            self.build_document(
                "doc-2"
            )
        )

        session.remove_document(
            "doc-1"
        )

        self.assertEqual(
            session.count(),
            1,
        )

        self.assertIsNotNone(

            session.get_document(
                "doc-2"
            )

        )

    # =====================================
    # LIST
    # =====================================

    def test_list_documents_returns_all(
        self,
    ):

        session = DocumentSession()

        session.add_document(
            self.build_document(
                "doc-1"
            )
        )

        session.add_document(
            self.build_document(
                "doc-2"
            )
        )

        documents = session.list_documents()

        self.assertEqual(
            len(documents),
            2,
        )

    def test_list_documents_preserves_insertion_order(
        self,
    ):

        session = DocumentSession()

        session.add_document(
            self.build_document(
                "A"
            )
        )

        session.add_document(
            self.build_document(
                "B"
            )
        )

        ids = [

            d.document_id

            for d in session.list_documents()

        ]

        self.assertEqual(

            ids,

            [
                "A",
                "B",
            ],

        )

    # =====================================
    # COUNT
    # =====================================

    def test_count_matches_documents(
        self,
    ):

        session = DocumentSession()

        for i in range(5):

            session.add_document(

                self.build_document(
                    f"doc-{i}"
                )

            )

        self.assertEqual(
            session.count(),
            5,
        )

    # =====================================
    # CLEAR
    # =====================================

    def test_clear_removes_everything(
        self,
    ):

        session = DocumentSession()

        session.add_document(
            self.build_document(
                "doc-1"
            )
        )

        session.add_document(
            self.build_document(
                "doc-2"
            )
        )

        session.clear()

        self.assertEqual(
            session.count(),
            0,
        )

        self.assertEqual(
            session.documents,
            {},
        )

    # =====================================
    # SERIALIZATION
    # =====================================

    def test_to_dict_empty(
        self,
    ):

        session = DocumentSession()

        payload = session.to_dict()

        self.assertEqual(

            payload,

            {
                "documents": [],
            },

        )

    def test_to_dict_contains_document(
        self,
    ):

        session = DocumentSession()

        session.add_document(
            self.build_document()
        )

        payload = session.to_dict()

        self.assertEqual(

            payload["documents"][0]["document_id"],

            "doc-1",

        )

        self.assertEqual(

            payload["documents"][0]["filename"],

            "paper.pdf",

        )

    def test_to_dict_preserves_pages(
        self,
    ):

        session = DocumentSession()

        session.add_document(
            self.build_document()
        )

        payload = session.to_dict()

        self.assertEqual(

            payload["documents"][0]["pages"],

            12,

        )

    def test_to_dict_preserves_chunks(
        self,
    ):

        session = DocumentSession()

        session.add_document(
            self.build_document()
        )

        payload = session.to_dict()

        self.assertEqual(

            payload["documents"][0]["chunks"],

            45,

        )

    def test_to_dict_preserves_content(
        self,
    ):

        session = DocumentSession()

        session.add_document(
            self.build_document()
        )

        payload = session.to_dict()

        self.assertEqual(

            payload["documents"][0]["content"],

            "example content",

        )

    def test_to_dict_preserves_pages_data(
        self,
    ):

        session = DocumentSession()

        session.add_document(
            self.build_document()
        )

        payload = session.to_dict()

        self.assertEqual(

            payload["documents"][0]["pages_data"],

            [
                {
                    "page": 1,
                }
            ],

        )