from __future__ import annotations


from delbot_platform.repository.auth.credential import (
    RepositoryCredential,
)


from delbot_platform.repository.auth.session import (
    RepositorySession,
)


from delbot_platform.repository.auth.gitlab_auth import (
    GitLabAuth,
)



class RepositoryAuthManager:
    """
    Repository authentication manager.

    Creates and stores authenticated sessions.
    """


    def __init__(
        self,
    ) -> None:

        self.sessions: dict[
            str,
            RepositorySession
        ] = {}



    def authenticate(
        self,
        repository_id: str,
        base_url: str,
        credential: RepositoryCredential,
    ) -> RepositorySession:


        session = RepositorySession()


        auth = GitLabAuth(
            base_url,
            session,
        )


        success = auth.login(
            credential,
        )


        if not success:

            raise PermissionError(
                "Repository authentication failed"
            )


        self.sessions[
            repository_id
        ] = session


        return session



    def get_session(
        self,
        repository_id: str,
    ) -> RepositorySession | None:

        return self.sessions.get(
            repository_id
        )



    def exists(
        self,
        repository_id: str,
    ) -> bool:

        return (
            repository_id
            in
            self.sessions
        )