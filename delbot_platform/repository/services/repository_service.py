from __future__ import annotations


from delbot_platform.repository.models import (
    Repository,
    Collection,
    RepositoryItem,
    Manifest,
)


from delbot_platform.repository.storage import (
    FilesystemRepositoryStorage,
)



class RepositoryService:
    """
    Repository domain service.

    Boundary between:

        API / Scanner / Workflow

                |

                v

        Repository Domain

                |

                v

        Storage Layer

    """


    def __init__(
        self,
        storage: FilesystemRepositoryStorage | None = None,
    ) -> None:


        self.storage = (

            storage

            if storage is not None

            else FilesystemRepositoryStorage()

        )



    #
    # Repository
    #

    def register_repository(
        self,
        repository: Repository,
    ) -> None:


        self.storage.save_repository(
            repository,
        )



    def get_repository(
        self,
        repository_id: str,
    ) -> Repository | None:


        return self.storage.load_repository(
            repository_id,
        )



    def exists(
        self,
        repository_id: str,
    ) -> bool:


        return self.storage.repository_exists(
            repository_id,
        )



    #
    # Collection
    #

    def register_collection(
        self,
        collection: Collection,
    ) -> None:


        self.storage.save_collection(
            collection,
        )



    def get_collection(
        self,
        collection_id: str,
    ) -> Collection | None:


        return self.storage.load_collection(
            collection_id,
        )



    #
    # Item
    #

    def register_item(
        self,
        item: RepositoryItem,
    ) -> None:


        self.storage.save_item(
            item,
        )



    def get_item(
        self,
        item_id: str,
    ) -> RepositoryItem | None:


        return self.storage.load_item(
            item_id,
        )



    def item_exists(
        self,
        item_id: str,
    ) -> bool:


        return self.storage.item_exists(
            item_id,
        )



    #
    # Manifest
    #

    def update_manifest(
        self,
        manifest: Manifest,
    ) -> None:


        self.storage.save_manifest(
            manifest,
        )



    def get_manifest(
        self,
        document_id: str,
    ) -> Manifest | None:


        return self.storage.load_manifest(
            document_id,
        )



    def processed(
        self,
        document_id: str,
    ) -> bool:


        manifest = self.get_manifest(
            document_id,
        )


        if manifest is None:

            return False


        return manifest.processed