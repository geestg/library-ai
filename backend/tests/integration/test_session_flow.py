from tests.integration.base import (
    IntegrationTestCase,
)


class SessionFlowTests(
    IntegrationTestCase,
):

    # =====================================
    # CREATE SESSION
    # =====================================

    def test_create_session_returns_workspace(
        self,
    ):

        payload = self.create_session()

        self.assertIn(
            "session_id",
            payload,
        )

        self.assertIn(
            "conversation",
            payload,
        )

        self.assertIn(
            "documents",
            payload,
        )

        self.assertIn(
            "workspace",
            payload,
        )

        self.assertIn(
            "execution",
            payload,
        )

    # =====================================
    # GET SESSION
    # =====================================

    def test_get_created_session(
        self,
    ):

        created = self.create_session()

        session_id = created[
            "session_id"
        ]

        response = self.client.get(
            f"/session/{session_id}"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        payload = response.json()

        self.assertEqual(
            payload["session_id"],
            session_id,
        )

    # =====================================
    # UNKNOWN SESSION
    # =====================================

    def test_unknown_session_returns_404(
        self,
    ):

        response = self.client.get(
            "/session/not-found"
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    # =====================================
    # DELETE SESSION
    # =====================================

    def test_delete_session(
        self,
    ):

        created = self.create_session()

        session_id = created[
            "session_id"
        ]

        response = self.client.delete(
            f"/session/{session_id}"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        verify = self.client.get(
            f"/session/{session_id}"
        )

        self.assertEqual(
            verify.status_code,
            404,
        )

    # =====================================
    # DELETE UNKNOWN
    # =====================================

    def test_delete_unknown_session(
        self,
    ):

        response = self.client.delete(
            "/session/not-found"
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    # =====================================
    # MULTIPLE SESSION IDS
    # =====================================

    def test_multiple_sessions_have_unique_ids(
        self,
    ):

        sessions = self.create_sessions(
            3
        )

        ids = {

            session["session_id"]

            for session in sessions

        }

        self.assertEqual(
            len(ids),
            3,
        )

    # =====================================
    # DELETE DOES NOT AFFECT OTHERS
    # =====================================

    def test_delete_one_session_keeps_others(
        self,
    ):

        sessions = self.create_sessions(
            3
        )

        a = sessions[0]["session_id"]

        b = sessions[1]["session_id"]

        c = sessions[2]["session_id"]

        self.client.delete(
            f"/session/{a}"
        )

        self.assertEqual(

            self.client.get(
                f"/session/{a}"
            ).status_code,

            404,

        )

        self.assertEqual(

            self.client.get(
                f"/session/{b}"
            ).status_code,

            200,

        )

        self.assertEqual(

            self.client.get(
                f"/session/{c}"
            ).status_code,

            200,

        )

    # =====================================
    # EMPTY SESSION
    # =====================================

    def test_new_session_has_empty_state(
        self,
    ):

        payload = self.create_session()

        conversation = payload[
            "conversation"
        ]

        documents = payload[
            "documents"
        ]

        execution = payload[
            "execution"
        ]

        self.assertEqual(
            conversation[
                "total_messages"
            ],
            0,
        )

        self.assertEqual(
            len(
                documents[
                    "documents"
                ]
            ),
            0,
        )

        self.assertEqual(
            execution[
                "last_query"
            ],
            "",
        )

        self.assertEqual(
            execution[
                "response"
            ],
            "",
        )