from __future__ import annotations


import httpx



class RepositorySession:
    """
    Persistent repository HTTP session.

    Responsible for:

    - cookies
    - headers
    - authenticated requests
    """


    def __init__(
        self,
        timeout: float = 30.0,
    ) -> None:


        self.client = httpx.Client(

            timeout=timeout,

            follow_redirects=False,

        )



    def get(
        self,
        url: str,
        **kwargs,
    ) -> httpx.Response:


        return self.client.get(

            url,

            **kwargs,

        )



    def post(
        self,
        url: str,
        data: dict | None = None,
        **kwargs,
    ) -> httpx.Response:


        return self.client.post(

            url,

            data=data,

            **kwargs,

        )



    def cookies(
        self,
    ):

        return self.client.cookies



    def authenticated(
        self,
    ) -> bool:


        return bool(
            self.client.cookies
        )