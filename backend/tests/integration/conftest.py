import pytest

from unittest.mock import MagicMock
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


# =====================================
# APPLICATION STARTUP PATCHES
# =====================================

@pytest.fixture(scope="session", autouse=True)
def patch_application_startup():

    with (
        patch(
            "app.main.initialize_database"
        ),

        patch(
            "app.main.register_prompts"
        ),

    ):

        yield


# =====================================
# TEST CLIENT
# =====================================

@pytest.fixture(scope="session")
def client():

    with TestClient(app) as test_client:

        yield test_client


# =====================================
# MOCK LLM EXECUTE
# =====================================

@pytest.fixture
def mock_llm_execute():

    with patch(

        "app.services.llm.tasks.llm_task.LLMTask.execute"

    ) as mock:

        mock.return_value = (
            "Mock LLM Response"
        )

        yield mock


# =====================================
# MOCK LLM STREAM
# =====================================

@pytest.fixture
def mock_llm_stream():

    with patch(

        "app.services.llm.tasks.llm_task.LLMTask.stream"

    ) as mock:

        mock.return_value = iter(

            [

                "Hello",

                " ",

                "World",

            ]

        )

        yield mock


# =====================================
# MOCK PDF INGESTION
# =====================================

@pytest.fixture
def mock_ingest_pdf():

    with patch(

        "app.api.routes.routes_upload.ingest_pdf"

    ) as mock:

        mock.return_value = {

            "pages": 5,

            "chunks": 12,

            "full_text":
                "Dummy document",

            "pages_data": [

                {

                    "page": 1,

                    "text":
                        "Dummy page",

                }

            ],

        }

        yield mock


# =====================================
# MOCK DOCUMENT RETRIEVAL
# =====================================

@pytest.fixture
def mock_document_chunks():

    with patch(

        "app.services.document.document_vector_retriever.retrieve_document_chunks"

    ) as mock:

        mock.return_value = [

            {

                "document_id":
                    "doc-001",

                "page":
                    1,

                "chunk_index":
                    0,

                "score":
                    0.98,

                "text":
                    "Dummy chunk",

            }

        ]

        yield mock


# =====================================
# MOCK RESEARCH ANALYSIS
# =====================================

@pytest.fixture
def mock_research_analysis():

    with patch(

        "app.api.routes.routes_chat_stream.research_analysis"

    ) as mock:

        context = MagicMock()

        context.session_id = (
            "integration-session"
        )

        context.provider = (
            "openrouter"
        )

        context.model = (
            "gpt-test"
        )

        context.intent = (
            "research"
        )

        context.analysis = ""

        context.response = None

        mock.return_value = (

            context,

            iter(

                [

                    "Hello",

                    " ",

                    "Integration",

                ]

            ),

        )

        yield mock


# =====================================
# MOCK SERIALIZER
# =====================================

@pytest.fixture
def mock_serializer():

    with patch(

        "app.api.routes.routes_chat_stream.serialize_research_context"

    ) as mock:

        mock.return_value = {

            "query":
                "integration",

            "analysis":
                "",

        }

        yield mock


# =====================================
# SAMPLE PDF CONTENT
# =====================================

@pytest.fixture
def pdf_bytes():

    return (
        b"%PDF-1.4\n"
        b"Dummy PDF\n"
        b"%%EOF"
    )