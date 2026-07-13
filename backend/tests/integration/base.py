import unittest

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


# =====================================
# BASE INTEGRATION TEST
# =====================================

class IntegrationTestCase(
    unittest.TestCase,
):

    client = None

    # =================================
    # CLASS SETUP
    # =================================

    @classmethod
    def setUpClass(
        cls,
    ):

        cls.database_patch = patch(
            "app.main.initialize_database"
        )

        cls.prompt_patch = patch(
            "app.main.register_prompts"
        )

        cls.database_patch.start()

        cls.prompt_patch.start()

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

        cls.client.close()

        cls.database_patch.stop()

        cls.prompt_patch.stop()

    # =================================
    # TEST SETUP
    # =================================

    def setUp(
        self,
    ):

        self.maxDiff = None

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