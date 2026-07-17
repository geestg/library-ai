from __future__ import annotations


import httpx


from delbot_platform.repository.auth.credential import (
    RepositoryCredential,
)


from delbot_platform.repository.auth.session import (
    RepositorySession,
)



class GitLabAuth:
    """
    Authentication handler for repository
    protected by GitLab/Rails session.

    Responsible for:

    - login request
    - session cookie persistence
    """


    def __init__(
        self,
        base_url: str,
        session: RepositorySession | None = None,
    ) -> None:


        self.base_url = (
            base_url.rstrip("/")
        )


        self.session = (

            session

            if session is not None

            else RepositorySession()

        )



    def login(
        self,
        credential: RepositoryCredential,
    ) -> bool:


        login_url = (
            f"{self.base_url}/users/sign_in"
        )


        response = self.session.client.get(
            login_url,
        )


        response.raise_for_status()


        cookies_before = (
            dict(
                self.session.cookies()
            )
        )


        login_data = {

            "user[login]":
                credential.username,

            "user[password]":
                credential.password,

        }


        response = (
            self.session.client.post(

                login_url,

                data=login_data,

            )
        )


        if response.status_code in (
            301,
            302,
            303,
            307,
            308,
        ):

            return True



        if self.session.authenticated():

            return True



        cookies_after = (
            dict(
                self.session.cookies()
            )
        )


        return (
            cookies_before
            !=
            cookies_after
        )
