from __future__ import annotations


import os


from delbot_platform.repository.auth.credential import (
    RepositoryCredential,
)



class EnvironmentCredentialProvider:
    """
    Loads repository credentials from environment.

    Naming convention:

        DELBOT_REPOSITORY_{ID}_USERNAME
        DELBOT_REPOSITORY_{ID}_PASSWORD

    Example:

        DELBOT_REPOSITORY_ITDEL_USERNAME

        DELBOT_REPOSITORY_ITDEL_PASSWORD

    """


    def load(
        self,
        repository_id: str,
    ) -> RepositoryCredential:


        prefix = (
            f"DELBOT_REPOSITORY_{repository_id.upper()}"
        )


        username = os.getenv(
            f"{prefix}_USERNAME",
            "",
        )


        password = os.getenv(
            f"{prefix}_PASSWORD",
            "",
        )


        return RepositoryCredential(

            username=username,

            password=password,

            repository_id=repository_id,

        )
