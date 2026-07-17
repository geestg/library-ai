from __future__ import annotations


import httpx


from delbot_platform.repository.dspace.client import (
    DSpaceClient,
)


from delbot_platform.repository.auth.session import (
    RepositorySession,
)



class DSpaceHTTPClient(
    DSpaceClient,
):
    """
    HTTP implementation for repository access.

    Handles:

    - HTTP communication
    - authentication session
    - response validation
    """



    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        session: RepositorySession | None = None,
    ) -> None:


        self.base_url = (
            base_url.rstrip("/")
        )


        self.session = (

            session

            if session is not None

            else RepositorySession(
                timeout=timeout,
            )

        )



    def _request(
        self,
        method: str,
        endpoint: str,
    ) -> httpx.Response:


        url = (
            f"{self.base_url}/{endpoint}"
        )


        print(
            "[REQUEST]",
            url,
        )


        try:

            response = (
                self.session.client.request(
                    method,
                    url,
                )
            )


        except httpx.TimeoutException as e:

            raise TimeoutError(
                f"Timeout accessing {url}"
            ) from e



        print(
            "[STATUS]",
            response.status_code,
        )


        print(
            "[LOCATION]",
            response.headers.get(
                "location"
            ),
        )


        return response



    def _json(
        self,
        endpoint: str,
    ) -> dict:


        response = self._request(
            "GET",
            endpoint,
        )


        if response.status_code in (
            301,
            302,
            303,
            307,
            308,
        ):

            raise PermissionError(
                response.headers.get(
                    "location"
                )
            )


        response.raise_for_status()


        return response.json()



    def get_item(
        self,
        item_id: str,
    ) -> dict:


        return self._json(
            f"server/api/core/items/{item_id}"
        )



    def get_metadata(
        self,
        item_id: str,
    ) -> dict:


        return self.get_item(
            item_id,
        )



    def get_files(
        self,
        item_id: str,
    ) -> list[dict]:


        data = self._json(
            f"server/api/core/items/{item_id}/bundles"
        )


        return data.get(
            "bundles",
            [],
        )



    def collections(
        self,
    ) -> list[dict]:


        data = self._json(
            "server/api/core/collections"
        )


        return data.get(
            "collections",
            [],
        )



    def items(
        self,
        collection_id: str,
    ) -> list[dict]:


        data = self._json(
            f"server/api/core/collections/{collection_id}/items"
        )


        return data.get(
            "items",
            [],
        )