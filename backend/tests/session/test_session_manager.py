import unittest

from tests.fakes import (
    FakeSessionRepository,
)

from app.services.research.session.session_manager import (
    SessionManager,
)

from app.services.research.session.models import (
    WorkspaceSession,
)

class SessionManagerTests(
    unittest.TestCase,
):

    def setUp(
        self,
    ):

        self.repository = (
            FakeSessionRepository()
        )

        self.manager = (
            SessionManager(
                repository=self.repository,
            )
        )

    # =====================================
    # CREATE
    # =====================================

    def test_create_returns_workspace_session(
        self,
    ):

        session = self.manager.create(
            "session-1",
        )

        self.assertIsInstance(
            session,
            WorkspaceSession,
        )

        self.assertEqual(
            session.session_id,
            "session-1",
        )

    def test_create_returns_existing_session(
        self,
    ):

        first = self.manager.create(
            "same-session",
        )

        second = self.manager.create(
            "same-session",
        )

        self.assertIs(
            first,
            second,
        )

        self.assertEqual(
            self.manager.count(),
            1,
        )

    def test_create_without_session_id_generates_identifier(
        self,
    ):

        session = self.manager.create()

        self.assertTrue(
            session.session_id,
        )

        self.assertEqual(
            self.manager.count(),
            1,
        )

    def test_create_blank_session_id_generates_identifier(
        self,
    ):

        session = self.manager.create(
            "   ",
        )

        self.assertTrue(
            session.session_id,
        )

    # =====================================
    # GET
    # =====================================

    def test_get_returns_existing_session(
        self,
    ):

        session = self.manager.create(
            "lookup",
        )

        loaded = self.manager.get(
            "lookup",
        )

        self.assertIs(
            session,
            loaded,
        )

    def test_get_unknown_returns_none(
        self,
    ):

        self.assertIsNone(
            self.manager.get(
                "missing",
            )
        )

    def test_get_empty_returns_none(
        self,
    ):

        self.assertIsNone(
            self.manager.get(
                "",
            )
        )

    # =====================================
    # GET OR CREATE
    # =====================================

    def test_get_or_create_returns_existing(
        self,
    ):

        session = self.manager.create(
            "existing",
        )

        loaded = self.manager.get_or_create(
            "existing",
        )

        self.assertIs(
            session,
            loaded,
        )

    def test_get_or_create_creates_missing(
        self,
    ):

        session = self.manager.get_or_create(
            "new-session",
        )

        self.assertEqual(
            session.session_id,
            "new-session",
        )

        self.assertEqual(
            self.manager.count(),
            1,
        )

    def test_get_or_create_without_id_creates_new_session(
        self,
    ):

        session = self.manager.get_or_create()

        self.assertTrue(
            session.session_id,
        )

    # =====================================
    # EXISTS
    # =====================================

    def test_exists_returns_true(
        self,
    ):

        self.manager.create(
            "exists",
        )

        self.assertTrue(
            self.manager.exists(
                "exists",
            )
        )

    def test_exists_returns_false(
        self,
    ):

        self.assertFalse(
            self.manager.exists(
                "missing",
            )
        )

    # =====================================
    # SAVE
    # =====================================

    def test_save_existing_session_returns_true(
        self,
    ):

        self.manager.create(
            "save-test",
        )

        self.assertTrue(
            self.manager.save(
                "save-test",
            )
        )

    def test_save_missing_session_returns_false(
        self,
    ):

        self.assertFalse(
            self.manager.save(
                "missing",
            )
        )

    # =====================================
    # DELETE
    # =====================================

    def test_delete_existing_session(
        self,
    ):

        self.manager.create(
            "delete-test",
        )

        deleted = self.manager.delete(
            "delete-test",
        )

        self.assertTrue(
            deleted,
        )

        self.assertFalse(
            self.manager.exists(
                "delete-test",
            )
        )

    def test_delete_unknown_returns_false(
        self,
    ):

        self.assertFalse(
            self.manager.delete(
                "missing",
            )
        )

    # =====================================
    # RESET
    # =====================================

    def test_reset_existing_session(
        self,
    ):

        session = self.manager.create(
            "reset-test",
        )

        session.conversation.append(
            role="user",
            content="hello",
        )

        self.assertTrue(
            self.manager.reset(
                "reset-test",
            )
        )

        self.assertEqual(
            session.conversation.total_messages(),
            0,
        )

    def test_reset_missing_session_returns_false(
        self,
    ):

        self.assertFalse(
            self.manager.reset(
                "missing",
            )
        )

    # =====================================
    # LIST
    # =====================================

    def test_list_session_ids_returns_all_sessions(
        self,
    ):

        self.manager.create(
            "a",
        )

        self.manager.create(
            "b",
        )

        ids = self.manager.list_session_ids()

        self.assertEqual(
            set(ids),
            {
                "a",
                "b",
            },
        )

    # =====================================
    # COUNT
    # =====================================

    def test_count_matches_created_sessions(
        self,
    ):

        self.manager.create(
            "1",
        )

        self.manager.create(
            "2",
        )

        self.manager.create(
            "3",
        )

        self.assertEqual(
            self.manager.count(),
            3,
        )

    # =====================================
    # CLEAR
    # =====================================

    def test_clear_removes_all_cached_sessions(
        self,
    ):

        self.manager.create(
            "one",
        )

        self.manager.create(
            "two",
        )

        self.assertEqual(
            self.manager.count(),
            2,
        )

        self.manager.clear()

        self.assertEqual(
            self.manager.count(),
            0,
        )

        self.assertEqual(
            self.manager.list_session_ids(),
            [],
        )


if __name__ == "__main__":
    unittest.main()