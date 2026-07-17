from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from delbot_platform.core.path_manager import (
    PathManager,
)

from delbot_platform.repository.models import (
    Repository,
    Collection,
    RepositoryItem,
    Manifest,
)


class FilesystemRepositoryStorage:
    """
    Filesystem based repository storage.

    Responsibility:

    - Persist repository metadata
    - Persist collection metadata
    - Persist repository items
    - Persist processing manifests

    Storage location:

        data/
            repository/

                repositories/
                collections/
                items/
                manifests/

    """

    def __init__(
        self,
        root: Path | None = None,
    ) -> None:

        self.root = (
            root
            if root is not None
            else PathManager.DATA / "repository"
        )

        self.repositories = (
            self.root / "repositories"
        )

        self.collections = (
            self.root / "collections"
        )

        self.items = (
            self.root / "items"
        )

        self.manifests = (
            self.root / "manifests"
        )

        self._ensure_directories()


    def _ensure_directories(
        self,
    ) -> None:

        for directory in [
            self.repositories,
            self.collections,
            self.items,
            self.manifests,
        ]:

            directory.mkdir(
                parents=True,
                exist_ok=True,
            )


    def _write_json(
        self,
        path: Path,
        data: dict,
    ) -> None:

        path.write_text(
            json.dumps(
                data,
                indent=2,
            ),
            encoding="utf-8",
        )


    def _read_json(
        self,
        path: Path,
    ) -> dict | None:

        if not path.exists():

            return None

        return json.loads(
            path.read_text(
                encoding="utf-8",
            )
        )


    #
    # Repository
    #

    def save_repository(
        self,
        repository: Repository,
    ) -> None:

        self._write_json(
            self.repositories
            / f"{repository.id}.json",

            asdict(
                repository,
            ),
        )


    def load_repository(
        self,
        repository_id: str,
    ) -> Repository | None:

        data = self._read_json(
            self.repositories
            / f"{repository_id}.json",
        )

        if data is None:

            return None

        return Repository(
            **data,
        )


    def repository_exists(
        self,
        repository_id: str,
    ) -> bool:

        return (
            self.repositories
            / f"{repository_id}.json"
        ).exists()


    #
    # Collection
    #

    def save_collection(
        self,
        collection: Collection,
    ) -> None:

        self._write_json(
            self.collections
            / f"{collection.id}.json",

            asdict(
                collection,
            ),
        )


    def load_collection(
        self,
        collection_id: str,
    ) -> Collection | None:

        data = self._read_json(
            self.collections
            / f"{collection_id}.json",
        )

        if data is None:

            return None

        return Collection(
            **data,
        )


    def collection_exists(
        self,
        collection_id: str,
    ) -> bool:

        return (
            self.collections
            / f"{collection_id}.json"
        ).exists()


    #
    # Repository Item
    #

    def save_item(
        self,
        item: RepositoryItem,
    ) -> None:

        self._write_json(
            self.items
            / f"{item.id}.json",

            asdict(
                item,
            ),
        )


    def load_item(
        self,
        item_id: str,
    ) -> RepositoryItem | None:

        data = self._read_json(
            self.items
            / f"{item_id}.json",
        )

        if data is None:

            return None

        return RepositoryItem(
            **data,
        )


    def item_exists(
        self,
        item_id: str,
    ) -> bool:

        return (
            self.items
            / f"{item_id}.json"
        ).exists()


    #
    # Manifest
    #

    def save_manifest(
        self,
        manifest: Manifest,
    ) -> None:

        self._write_json(
            self.manifests
            / f"{manifest.document_id}.json",

            asdict(
                manifest,
            ),
        )


    def load_manifest(
        self,
        document_id: str,
    ) -> Manifest | None:

        data = self._read_json(
            self.manifests
            / f"{document_id}.json",
        )

        if data is None:

            return None

        return Manifest(
            **data,
        )


    def manifest_exists(
        self,
        document_id: str,
    ) -> bool:

        return (
            self.manifests
            / f"{document_id}.json"
        ).exists()