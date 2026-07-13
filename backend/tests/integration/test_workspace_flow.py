import io

from app.services.research.session import (
    session_manager,
)


class TestWorkspaceFlow:

    def test_complete_workspace_lifecycle(

        self,

        client,

        mock_ingest_pdf,

        mock_llm_execute,

        mock_llm_stream,

        mock_research_analysis,

        mock_serializer,

        pdf_bytes,

    ):

        # =====================================
        # CREATE SESSION
        # =====================================

        response = client.post(
            "/session/create"
        )

        assert response.status_code == 200

        session = response.json()

        session_id = session[
            "session_id"
        ]

        assert session_id

        # =====================================
        # UPLOAD DOCUMENT
        # =====================================

        upload = client.post(

            "/upload-pdf",

            files={

                "file": (

                    "paper.pdf",

                    io.BytesIO(
                        pdf_bytes
                    ),

                    "application/pdf",

                ),

            },

            data={

                "session_id":
                    session_id,

            },

        )

        assert upload.status_code == 200

        upload_json = upload.json()

        document_id = upload_json[
            "document_id"
        ]

        assert document_id

        # =====================================
        # DOCUMENT EXISTS
        # =====================================

        workspace = (
            session_manager.get(
                session_id
            )
        )

        assert workspace is not None

        assert (

            workspace.documents.count()

            == 1

        )

        # =====================================
        # LIST DOCUMENTS
        # =====================================

        listing = client.get(

            f"/session/{session_id}/documents"

        )

        assert listing.status_code == 200

        payload = listing.json()

        assert (

            payload[
                "total_documents"
            ]

            == 1

        )

        # =====================================
        # DOCUMENT CHAT
        # =====================================

        chat = client.post(

            "/document/chat",

            json={

                "session_id":
                    session_id,

                "document_id":
                    document_id,

                "question":
                    "Ringkas dokumen",

            },

        )

        assert chat.status_code == 200

        chat_payload = (
            chat.json()
        )

        assert (

            chat_payload[
                "answer"
            ]

            == "Mock LLM Response"

        )

        # =====================================
        # STREAM CHAT
        # =====================================

        stream = client.post(

            "/chat-stream",

            json={

                "session_id":
                    session_id,

                "message":
                    "Jelaskan dokumen",

                "active_document_ids": [

                    document_id,

                ],

            },

        )

        assert stream.status_code == 200

        body = stream.text

        assert (
            '"type": "start"'
            in body
        )

        assert (
            '"type": "metadata"'
            in body
        )

        assert (
            '"type": "context"'
            in body
        )

        assert (
            '"type": "token"'
            in body
        )

        assert (
            '"type": "context_final"'
            in body
        )

        assert (
            '"type": "end"'
            in body
        )

        # =====================================
        # DELETE DOCUMENT
        # =====================================

        delete = client.delete(

            f"/session/{session_id}"
            f"/documents/{document_id}"

        )

        assert delete.status_code == 200

        workspace = (
            session_manager.get(
                session_id
            )
        )

        assert (

            workspace.documents.count()

            == 0

        )

        # =====================================
        # DOCUMENT LIST EMPTY
        # =====================================

        listing = client.get(

            f"/session/{session_id}/documents"

        )

        assert (

            listing.json()[
                "total_documents"
            ]

            == 0

        )

        # =====================================
        # DELETE SESSION
        # =====================================

        deleted = client.delete(

            f"/session/{session_id}"

        )

        assert deleted.status_code == 200

        # =====================================
        # VERIFY SESSION REMOVED
        # =====================================

        missing = client.get(

            f"/session/{session_id}"

        )

        assert (

            missing.status_code

            == 404

        )