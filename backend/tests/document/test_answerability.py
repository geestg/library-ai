import unittest
from unittest.mock import patch

from app.services.research.engines.document_engine import (
    ANSWERABLE,
    NOT_FOUND,
    build_not_found_response,
    normalize_answerability,
    verify_answerability,
)


class NormalizeAnswerabilityTests(
    unittest.TestCase,
):

    def test_exact_answerable(
        self,
    ):

        self.assertEqual(
            normalize_answerability(
                "ANSWERABLE"
            ),
            ANSWERABLE,
        )

    def test_exact_not_found(
        self,
    ):

        self.assertEqual(
            normalize_answerability(
                "NOT_FOUND"
            ),
            NOT_FOUND,
        )

    def test_lowercase_answerable(
        self,
    ):

        self.assertEqual(
            normalize_answerability(
                "answerable"
            ),
            ANSWERABLE,
        )

    def test_lowercase_not_found(
        self,
    ):

        self.assertEqual(
            normalize_answerability(
                "not_found"
            ),
            NOT_FOUND,
        )

    def test_answerable_with_spaces(
        self,
    ):

        self.assertEqual(
            normalize_answerability(
                "   ANSWERABLE   "
            ),
            ANSWERABLE,
        )

    def test_multiline_answerable(
        self,
    ):

        self.assertEqual(
            normalize_answerability(
                "Result\nANSWERABLE\nDone"
            ),
            ANSWERABLE,
        )

    def test_multiline_not_found(
        self,
    ):

        self.assertEqual(
            normalize_answerability(
                "Reason\nNOT_FOUND\nDone"
            ),
            NOT_FOUND,
        )

    def test_none_returns_not_found(
        self,
    ):

        self.assertEqual(
            normalize_answerability(
                None
            ),
            NOT_FOUND,
        )

    def test_empty_returns_not_found(
        self,
    ):

        self.assertEqual(
            normalize_answerability(
                ""
            ),
            NOT_FOUND,
        )

    def test_unknown_returns_not_found(
        self,
    ):

        self.assertEqual(
            normalize_answerability(
                "SOMETHING_ELSE"
            ),
            NOT_FOUND,
        )


class BuildNotFoundResponseTests(
    unittest.TestCase,
):

    def test_response_contains_query(
        self,
    ):

        response = build_not_found_response(
            query="apa tujuan penelitian",
            documents=[],
            chunks=[],
        )

        self.assertEqual(
            response["query"],
            "apa tujuan penelitian",
        )

    def test_answerability_is_not_found(
        self,
    ):

        response = build_not_found_response(
            query="q",
            documents=[],
            chunks=[],
        )

        self.assertEqual(
            response["answerability"],
            NOT_FOUND,
        )

    def test_citation_chunks_empty(
        self,
    ):

        response = build_not_found_response(
            query="q",
            documents=[],
            chunks=[
                {
                    "id": 1,
                }
            ],
        )

        self.assertEqual(
            response["citation_chunks"],
            [],
        )

    def test_documents_are_preserved(
        self,
    ):

        docs = [
            {
                "document_id": "doc1",
            }
        ]

        response = build_not_found_response(
            query="q",
            documents=docs,
            chunks=[],
        )

        self.assertEqual(
            response["documents"],
            docs,
        )

    def test_retrieved_chunks_are_preserved(
        self,
    ):

        chunks = [
            {
                "chunk": 1,
            }
        ]

        response = build_not_found_response(
            query="q",
            documents=[],
            chunks=chunks,
        )

        self.assertEqual(
            response["retrieved_chunks"],
            chunks,
        )


class VerifyAnswerabilityTests(
    unittest.TestCase,
):

    def setUp(
        self,
    ):

        self.documents = [

            {
                "document_id": "doc1",
                "filename": "paper.pdf",
            }

        ]

        self.chunks = [

            {
                "document_id": "doc1",
                "page": 1,
                "chunk_index": 0,
                "score": 0.95,
                "text": "Artificial Intelligence",
            }

        ]

    def test_empty_chunks_returns_not_found(
        self,
    ):

        result = verify_answerability(

            query="AI",

            chunks=[],

            documents=self.documents,

        )

        self.assertEqual(
            result["status"],
            NOT_FOUND,
        )

    @patch(
        "app.services.research.engines.document_engine.verify_single_chunk"
    )
    def test_single_chunk_answerable(
        self,
        mock_verify,
    ):

        mock_verify.return_value = ANSWERABLE

        result = verify_answerability(

            query="AI",

            chunks=self.chunks,

            documents=self.documents,

        )

        self.assertEqual(
            result["status"],
            ANSWERABLE,
        )

        self.assertEqual(
            result["verification_mode"],
            "per_chunk",
        )

        self.assertEqual(
            len(
                result["answerable_chunks"]
            ),
            1,
        )

    @patch(
        "app.services.research.engines.document_engine.verify_collective_context"
    )
    @patch(
        "app.services.research.engines.document_engine.verify_single_chunk"
    )
    def test_collective_answerable(
        self,
        mock_single,
        mock_collective,
    ):

        mock_single.return_value = NOT_FOUND

        mock_collective.return_value = ANSWERABLE

        result = verify_answerability(

            query="AI",

            chunks=self.chunks,

            documents=self.documents,

        )

        self.assertEqual(
            result["status"],
            ANSWERABLE,
        )

        self.assertEqual(
            result["verification_mode"],
            "collective",
        )

    @patch(
        "app.services.research.engines.document_engine.verify_collective_context"
    )
    @patch(
        "app.services.research.engines.document_engine.verify_single_chunk"
    )
    def test_collective_not_found(
        self,
        mock_single,
        mock_collective,
    ):

        mock_single.return_value = NOT_FOUND

        mock_collective.return_value = NOT_FOUND

        result = verify_answerability(

            query="AI",

            chunks=self.chunks,

            documents=self.documents,

        )

        self.assertEqual(
            result["status"],
            NOT_FOUND,
        )

        self.assertEqual(
            result["verification_mode"],
            "none",
        )

    @patch(
        "app.services.research.engines.document_engine.verify_single_chunk"
    )
    def test_multiple_answerable_chunks(
        self,
        mock_verify,
    ):

        mock_verify.return_value = ANSWERABLE

        chunks = self.chunks * 2

        result = verify_answerability(

            query="AI",

            chunks=chunks,

            documents=self.documents,

        )

        self.assertEqual(
            len(
                result["answerable_chunks"]
            ),
            2,
        )