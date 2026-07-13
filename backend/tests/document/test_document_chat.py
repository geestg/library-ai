import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.routes_document import (
    router,
)

from app.services.research.session.models.document_session import (
    DocumentItem,
)

from app.services.research.session.models.document_session import (
    DocumentSession,
)

from app.services.research.session.models.workspace_session import (
    WorkspaceSession,
)

from app.services.research.session.models.conversation_session import (
    ConversationSession,
)

from app.services.research.session.models.workspace_state import (
    WorkspaceState,
)

from app.services.research.session.models.execution_session import (
    ExecutionSession,
)


# =====================================
# TEST APPLICATION
# =====================================

app = FastAPI()

app.include_router(router)

client = TestClient(app)


# =====================================
# HELPERS
# =====================================

def build_workspace_session():

    return WorkspaceSession(

        session_id="session-1",

        conversation=ConversationSession(),

        documents=DocumentSession(),

        workspace=WorkspaceState(),

        execution=ExecutionSession(),

    )


def add_document(

    session,

    document_id="doc-1",

    filename="guide.pdf",

):

    document = DocumentItem(

        document_id=document_id,

        filename=filename,

        file_type="pdf",

        pages=10,

        chunks=20,

        content=(

            "This is the complete "

            "document content."

        ),

        pages_data=[

            {

                "page": 1,

                "text": (

                    "Installation guide"

                ),

            },

            {

                "page": 2,

                "text": (

                    "System requirements"

                ),

            },

        ],

    )

    session.documents.add_document(
        document
    )

    return document


# =====================================
# DOCUMENT CHAT TESTS
# =====================================

class DocumentChatTests(
    unittest.TestCase,
):

    def setUp(
        self,
    ):

        self.session = (
            build_workspace_session()
        )

        self.document = (
            add_document(
                self.session
            )
        )

    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_unknown_session_returns_404(

        self,

        mock_manager,

    ):

        mock_manager.get.return_value = None

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    "missing",

                "document_id":
                    "doc-1",

                "question":
                    "Apa isi dokumen?",

            },

        )

        self.assertEqual(

            response.status_code,

            404,

        )

        self.assertEqual(

            response.json()["detail"],

            "Session not found",

        )

    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_unknown_document_returns_404(

        self,

        mock_manager,

    ):

        mock_manager.get.return_value = (
            self.session
        )

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    self.session.session_id,

                "document_id":
                    "missing",

                "question":
                    "Apa isi dokumen?",

            },

        )

        self.assertEqual(

            response.status_code,

            404,

        )

        self.assertEqual(

            response.json()["detail"],

            "Document not found",

        )

    @patch(
    "app.api.routes.routes_document.LLMTask.execute"
    )
    @patch(
        "app.api.routes.routes_document.PromptRegistry.build_request"
    )
    @patch(
        "app.api.routes.routes_document.retrieve_relevant_chunks"
    )
    @patch(
        "app.api.routes.routes_document.detect_document_intent"
    )
    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_default_question_returns_answer(

        self,

        mock_manager,

        mock_detect,

        mock_retrieve,

        mock_prompt,

        mock_execute,

    ):

        mock_manager.get.return_value = (
            self.session
        )

        mock_detect.return_value = (
            "question"
        )

        mock_retrieve.return_value = [

            {

                "page": 1,

                "text":
                    "Artificial Intelligence adalah bidang ilmu komputer.",

            }

        ]

        mock_prompt.return_value = (
            MagicMock()
        )

        mock_execute.return_value = (
            "Jawaban AI"
        )

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    self.session.session_id,

                "document_id":
                    self.document.document_id,

                "question":
                    "Apa itu Artificial Intelligence?",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        payload = response.json()

        self.assertEqual(
            payload["answer"],
            "Jawaban AI",
        )

        self.assertEqual(
            payload["intent"],
            "question",
        )

        self.assertEqual(
            payload["filename"],
            self.document.filename,
        )

        self.assertEqual(
            payload["retrieved_chunks"],
            1,
        )

        mock_detect.assert_called_once()

        mock_retrieve.assert_called_once()

        mock_prompt.assert_called_once()

        mock_execute.assert_called_once()

    @patch(
        "app.api.routes.routes_document.LLMTask.execute"
    )
    @patch(
        "app.api.routes.routes_document.PromptRegistry.build_request"
    )
    @patch(
        "app.api.routes.routes_document.retrieve_relevant_chunks"
    )
    @patch(
        "app.api.routes.routes_document.detect_document_intent"
    )
    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_summary_intent_uses_summary_instruction(

        self,

        mock_manager,

        mock_detect,

        mock_retrieve,

        mock_prompt,

        mock_execute,

    ):

        mock_manager.get.return_value = (
            self.session
        )

        mock_detect.return_value = (
            "summary"
        )

        mock_retrieve.return_value = [

            {

                "page": 1,

                "text":
                    "Isi halaman pertama.",

            }

        ]

        captured_prompt = {}

        def fake_build_request(
            prompt_type,
            prompt,
        ):

            captured_prompt[
                "prompt"
            ] = prompt

            return MagicMock()

        mock_prompt.side_effect = (
            fake_build_request
        )

        mock_execute.return_value = (
            "Ringkasan"
        )

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    self.session.session_id,

                "document_id":
                    self.document.document_id,

                "question":
                    "Ringkas dokumen",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertIn(

            "Buat ringkasan dokumen",

            captured_prompt[
                "prompt"
            ],

        )

        self.assertEqual(

            response.json()[
                "intent"
            ],

            "summary",

        )

    @patch(
        "app.api.routes.routes_document.LLMTask.execute"
    )
    @patch(
        "app.api.routes.routes_document.PromptRegistry.build_request"
    )
    @patch(
        "app.api.routes.routes_document.retrieve_relevant_chunks"
    )
    @patch(
        "app.api.routes.routes_document.detect_document_intent"
    )
    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_timeline_intent_uses_timeline_instruction(

        self,

        mock_manager,

        mock_detect,

        mock_retrieve,

        mock_prompt,

        mock_execute,

    ):

        mock_manager.get.return_value = (
            self.session
        )

        mock_detect.return_value = (
            "timeline"
        )

        mock_retrieve.return_value = [

            {

                "page": 3,

                "text":
                    "Timeline penelitian.",

            }

        ]

        captured_prompt = {}

        def fake_build_request(
            prompt_type,
            prompt,
        ):

            captured_prompt[
                "prompt"
            ] = prompt

            return MagicMock()

        mock_prompt.side_effect = (
            fake_build_request
        )

        mock_execute.return_value = (
            "Timeline"
        )

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    self.session.session_id,

                "document_id":
                    self.document.document_id,

                "question":
                    "Buat timeline",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertIn(

            "Ekstrak seluruh timeline",

            captured_prompt[
                "prompt"
            ],

        )

        self.assertIn(

            "format tabel markdown",

            captured_prompt[
                "prompt"
            ].lower(),

        )

        self.assertEqual(

            response.json()[
                "intent"
            ],

            "timeline",

        )
    @patch(
        "app.api.routes.routes_document.LLMTask.execute"
    )
    @patch(
        "app.api.routes.routes_document.PromptRegistry.build_request"
    )
    @patch(
        "app.api.routes.routes_document.retrieve_relevant_chunks"
    )
    @patch(
        "app.api.routes.routes_document.detect_document_intent"
    )
    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_requirements_intent_uses_requirement_instruction(

        self,

        mock_manager,

        mock_detect,

        mock_retrieve,

        mock_prompt,

        mock_execute,

    ):

        mock_manager.get.return_value = (
            self.session
        )

        mock_detect.return_value = (
            "requirements"
        )

        mock_retrieve.return_value = [

            {

                "page": 2,

                "text":
                    "Minimal RAM 8 GB.",

            }

        ]

        captured_prompt = {}

        def fake_build_request(
            prompt_type,
            prompt,
        ):

            captured_prompt["prompt"] = (
                prompt
            )

            return MagicMock()

        mock_prompt.side_effect = (
            fake_build_request
        )

        mock_execute.return_value = (
            "Requirements"
        )

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    self.session.session_id,

                "document_id":
                    self.document.document_id,

                "question":
                    "Apa saja persyaratannya?",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertIn(

            "Ekstrak seluruh syarat",

            captured_prompt[
                "prompt"
            ],

        )

        self.assertEqual(

            response.json()[
                "intent"
            ],

            "requirements",

        )

    @patch(
        "app.api.routes.routes_document.LLMTask.execute"
    )
    @patch(
        "app.api.routes.routes_document.PromptRegistry.build_request"
    )
    @patch(
        "app.api.routes.routes_document.retrieve_relevant_chunks"
    )
    @patch(
        "app.api.routes.routes_document.detect_document_intent"
    )
    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_checklist_intent_uses_checklist_instruction(

        self,

        mock_manager,

        mock_detect,

        mock_retrieve,

        mock_prompt,

        mock_execute,

    ):

        mock_manager.get.return_value = (
            self.session
        )

        mock_detect.return_value = (
            "checklist"
        )

        mock_retrieve.return_value = [

            {

                "page": 5,

                "text":
                    "Siapkan proposal.",

            }

        ]

        captured_prompt = {}

        def fake_build_request(
            prompt_type,
            prompt,
        ):

            captured_prompt["prompt"] = (
                prompt
            )

            return MagicMock()

        mock_prompt.side_effect = (
            fake_build_request
        )

        mock_execute.return_value = (
            "Checklist"
        )

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    self.session.session_id,

                "document_id":
                    self.document.document_id,

                "question":
                    "Buat checklist",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertIn(

            "checklist",

            captured_prompt[
                "prompt"
            ].lower(),

        )

        self.assertEqual(

            response.json()[
                "intent"
            ],

            "checklist",

        )

    @patch(
        "app.api.routes.routes_document.LLMTask.execute"
    )
    @patch(
        "app.api.routes.routes_document.PromptRegistry.build_request"
    )
    @patch(
        "app.api.routes.routes_document.retrieve_relevant_chunks"
    )
    @patch(
        "app.api.routes.routes_document.detect_document_intent"
    )
    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_deliverables_intent_uses_deliverables_instruction(

        self,

        mock_manager,

        mock_detect,

        mock_retrieve,

        mock_prompt,

        mock_execute,

    ):

        mock_manager.get.return_value = (
            self.session
        )

        mock_detect.return_value = (
            "deliverables"
        )

        mock_retrieve.return_value = [

            {

                "page": 7,

                "text":
                    "Proposal dan video.",

            }

        ]

        captured_prompt = {}

        def fake_build_request(
            prompt_type,
            prompt,
        ):

            captured_prompt["prompt"] = (
                prompt
            )

            return MagicMock()

        mock_prompt.side_effect = (
            fake_build_request
        )

        mock_execute.return_value = (
            "Deliverables"
        )

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    self.session.session_id,

                "document_id":
                    self.document.document_id,

                "question":
                    "Apa saja deliverables?",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertIn(

            "proposal",

            captured_prompt[
                "prompt"
            ].lower(),

        )

        self.assertIn(

            "submission",

            captured_prompt[
                "prompt"
            ].lower(),

        )

        self.assertEqual(

            response.json()[
                "intent"
            ],

            "deliverables",

        )

    @patch(
        "app.api.routes.routes_document.LLMTask.execute"
    )
    @patch(
        "app.api.routes.routes_document.PromptRegistry.build_request"
    )
    @patch(
        "app.api.routes.routes_document.retrieve_relevant_chunks"
    )
    @patch(
        "app.api.routes.routes_document.detect_document_intent"
    )
    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_empty_chunk_result_falls_back_to_document_content(

        self,

        mock_manager,

        mock_detect,

        mock_retrieve,

        mock_prompt,

        mock_execute,

    ):

        mock_manager.get.return_value = (
            self.session
        )

        mock_detect.return_value = (
            "question"
        )

        mock_retrieve.return_value = []

        captured_prompt = {}

        def fake_build_request(
            prompt_type,
            prompt,
        ):

            captured_prompt[
                "prompt"
            ] = prompt

            return MagicMock()

        mock_prompt.side_effect = (
            fake_build_request
        )

        mock_execute.return_value = (
            "Fallback Answer"
        )

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    self.session.session_id,

                "document_id":
                    self.document.document_id,

                "question":
                    "Isi dokumen?",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertIn(

            self.document.content,

            captured_prompt[
                "prompt"
            ],

        )

        self.assertEqual(

            response.json()[
                "retrieved_chunks"
            ],

            0,

        )
    @patch(
        "app.api.routes.routes_document.LLMTask.execute"
    )
    @patch(
        "app.api.routes.routes_document.PromptRegistry.build_request"
    )
    @patch(
        "app.api.routes.routes_document.retrieve_relevant_chunks"
    )
    @patch(
        "app.api.routes.routes_document.detect_document_intent"
    )
    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_prompt_contains_page_information(

        self,

        mock_manager,

        mock_detect,

        mock_retrieve,

        mock_prompt,

        mock_execute,

    ):

        mock_manager.get.return_value = (
            self.session
        )

        mock_detect.return_value = (
            "question"
        )

        mock_retrieve.return_value = [

            {

                "page": 3,

                "text":
                    "Halaman tiga",

            },

            {

                "page": 7,

                "text":
                    "Halaman tujuh",

            },

        ]

        captured_prompt = {}

        def fake_build_request(

            prompt_type,

            prompt,

        ):

            captured_prompt[
                "prompt"
            ] = prompt

            return MagicMock()

        mock_prompt.side_effect = (
            fake_build_request
        )

        mock_execute.return_value = (
            "Answer"
        )

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    self.session.session_id,

                "document_id":
                    self.document.document_id,

                "question":
                    "Apa isi dokumen?",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        prompt = captured_prompt[
            "prompt"
        ]

        self.assertIn(
            "[PAGE 3]",
            prompt,
        )

        self.assertIn(
            "[PAGE 7]",
            prompt,
        )

    @patch(
        "app.api.routes.routes_document.LLMTask.execute"
    )
    @patch(
        "app.api.routes.routes_document.PromptRegistry.build_request"
    )
    @patch(
        "app.api.routes.routes_document.retrieve_relevant_chunks"
    )
    @patch(
        "app.api.routes.routes_document.detect_document_intent"
    )
    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_llm_is_called_once(

        self,

        mock_manager,

        mock_detect,

        mock_retrieve,

        mock_prompt,

        mock_execute,

    ):

        mock_manager.get.return_value = (
            self.session
        )

        mock_detect.return_value = (
            "question"
        )

        mock_retrieve.return_value = []

        mock_prompt.return_value = (
            MagicMock()
        )

        mock_execute.return_value = (
            "Answer"
        )

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    self.session.session_id,

                "document_id":
                    self.document.document_id,

                "question":
                    "Pertanyaan",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        mock_execute.assert_called_once()

    @patch(
        "app.api.routes.routes_document.LLMTask.execute"
    )
    @patch(
        "app.api.routes.routes_document.PromptRegistry.build_request"
    )
    @patch(
        "app.api.routes.routes_document.retrieve_relevant_chunks"
    )
    @patch(
        "app.api.routes.routes_document.detect_document_intent"
    )
    @patch(
        "app.api.routes.routes_document.session_manager"
    )
    def test_response_contract(

        self,

        mock_manager,

        mock_detect,

        mock_retrieve,

        mock_prompt,

        mock_execute,

    ):

        mock_manager.get.return_value = (
            self.session
        )

        mock_detect.return_value = (
            "question"
        )

        mock_retrieve.return_value = []

        mock_prompt.return_value = (
            MagicMock()
        )

        mock_execute.return_value = (
            "Final Answer"
        )

        response = client.post(

            "/document/chat",

            json={

                "session_id":
                    self.session.session_id,

                "document_id":
                    self.document.document_id,

                "question":
                    "Apa isi dokumen?",

            },

        )

        self.assertEqual(
            response.status_code,
            200,
        )

        payload = response.json()

        self.assertSetEqual(

            set(payload.keys()),

            {

                "answer",

                "filename",

                "intent",

                "retrieved_chunks",

            },

        )

        self.assertEqual(

            payload["answer"],

            "Final Answer",

        )

        self.assertEqual(

            payload["filename"],

            self.document.filename,

        )

        self.assertEqual(

            payload["intent"],

            "question",

        )

        self.assertEqual(

            payload["retrieved_chunks"],

            0,

        )


if __name__ == "__main__":

    unittest.main()