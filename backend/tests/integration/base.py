import unittest

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

from app.services.prompts.registry import (
    PromptRegistry,
)

from app.services.prompts.register_prompts import (
    register_prompts,
)

from app.services.research.session.session_manager import (
    SessionManager,
)

from tests.integration.fake_session_repository import (
    FakeSessionRepository,
)


# =====================================
# BASE INTEGRATION TEST
# =====================================

class IntegrationTestCase(
    unittest.TestCase,
):

    client = None

    fake_repository = None

    session_manager = None

    patches = []

    # =================================
    # CLASS SETUP
    # =================================

    @classmethod
    def setUpClass(
        cls,
    ):

        cls.patches = []

        # ==============================
        # PATCH APPLICATION STARTUP
        # ==============================

        startup_targets = [

            "app.main.initialize_database",

        ]

        for target in startup_targets:

            patcher = patch(
                target
            )

            patcher.start()

            cls.patches.append(
                patcher
            )

        # ==============================
        # INITIALIZE PROMPT REGISTRY
        # ==============================

        PromptRegistry.clear()

        register_prompts()

        # ==============================
        # BUILD FAKE SESSION MANAGER
        # ==============================

        cls.fake_repository = (
            FakeSessionRepository()
        )

        cls.session_manager = (
            SessionManager(
                repository=(
                    cls.fake_repository
                )
            )
        )

        # ==============================
        # PATCH SHARED SESSION MANAGER
        # ==============================

        singleton_targets = [

            # REST

            "app.api.routes.routes_session.session_manager",

            "app.api.routes.routes_upload.session_manager",

            "app.api.routes.routes_document.session_manager",

            "app.api.routes.routes_chat_stream.session_manager",

            # Research

            "app.services.research.research_engine.session_manager",

            # Document Engine

            "app.services.research.engines.document_engine.session_manager",

        ]

        for target in singleton_targets:

            patcher = patch(

                target,

                cls.session_manager,

            )

            patcher.start()

            cls.patches.append(
                patcher
            )

        # ==============================
        # TEST CLIENT
        # ==============================

        cls.client = TestClient(
            app
        )

    # =================================
    # CLASS TEARDOWN
    # =================================

    @classmethod
    def tearDownClass(
        cls,
    ):

        if cls.client is not None:

            cls.client.close()

        for patcher in reversed(
            cls.patches
        ):

            patcher.stop()

        # ==============================
        # RESET PROMPT REGISTRY
        # ==============================

        PromptRegistry.clear()

    # =================================
    # TEST SETUP
    # =================================

    def setUp(
        self,
    ):

        self.maxDiff = None

        self.fake_repository.clear()

        self.session_manager.clear()

    # =================================
    # CREATE SESSION
    # =================================

    def create_session(
        self,
    ):

        response = self.client.post(
            "/session/create"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        return response.json()

    # =================================
    # CREATE MULTIPLE SESSIONS
    # =================================

    def create_sessions(
        self,
        count: int,
    ):

        return [

            self.create_session()

            for _ in range(count)

        ]

    # =================================
    # PATCH HELPER
    # =================================

    def start_patch(

        self,

        target: str,

        return_value=None,

    ):

        patcher = patch(
            target
        )

        mocked = patcher.start()

        self.addCleanup(
            patcher.stop
        )

        if return_value is not None:

            mocked.return_value = (
                return_value
            )

        return mocked