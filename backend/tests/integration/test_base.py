from tests.integration.base import (
    IntegrationTestCase,
)


class IntegrationBaseTests(
    IntegrationTestCase,
):

    def test_client_created(
        self,
    ):

        self.assertIsNotNone(
            self.client
        )

    def test_root_endpoint(
        self,
    ):

        response = self.client.get(
            "/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        payload = response.json()

        self.assertEqual(
            payload["status"],
            "running",
        )

        self.assertEqual(
            payload["system"],
            "DELBot",
        )