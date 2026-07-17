from __future__ import annotations


from delbot_platform.repository import (
    RepositoryService,
    RepositoryIndexService,
)



class RepositoryAPIService:


    def __init__(
        self,
        repository_service: RepositoryService | None = None,
        index_service: RepositoryIndexService | None = None,
    ) -> None:


        self.repository_service = (

            repository_service

            if repository_service is not None

            else RepositoryService()

        )


        self.index_service = (

            index_service

            if index_service is not None

            else RepositoryIndexService()

        )



    #
    # Repository
    #

    def register(
        self,
        repository,
    ):


        return (
            self.repository_service
            .register_repository(
                repository,
            )
        )



    def exists(
        self,
        repository_id: str,
    ) -> bool:


        return (
            self.repository_service
            .exists(
                repository_id,
            )
        )



    #
    # Indexing
    #

    async def index(
        self,
        item_id: str,
    ):


        return await (
            self.index_service
            .index(
                item_id,
            )
        )