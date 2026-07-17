from __future__ import annotations


from pathlib import Path

import yaml


from delbot_platform.repository.auth.credential import (
    RepositoryCredential,
)



class RepositoryCredentialLoader:
    """
    Loads repository credentials.

    Source:

        config/repository.yaml

    """


    def __init__(
        self,
        path: str | Path,
    ) -> None:


        self.path = Path(
            path
        )



    def load(
        self,
        repository_id: str,
    ) -> RepositoryCredential:


        if not self.path.exists():

            raise FileNotFoundError(
                self.path
            )


        data = yaml.safe_load(

            self.path.read_text(
                encoding="utf-8",
            )

        )


        repositories = (

            data.get(
                "repositories",
                {},
            )

        )


        repository = repositories.get(
            repository_id,
        )


        if repository is None:

            raise KeyError(
                f"Repository credential not found: {repository_id}"
            )



        return RepositoryCredential(

            repository_id=repository_id,

            username=repository.get(
                "username",
                "",
            ),

            password=repository.get(
                "password",
                "",
            ),

        )