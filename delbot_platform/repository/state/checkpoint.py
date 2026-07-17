from __future__ import annotations

import json

from dataclasses import asdict

from pathlib import Path


from delbot_platform.repository.state.document_state import (
    DocumentState,
    DocumentStatus,
)



class CheckpointManager:
    """
    Persistent checkpoint storage.

    Used for resume capability.
    """


    def __init__(
        self,
        root: str | Path = "runtime/repository",
    ) -> None:


        self.root = Path(
            root,
        )


        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )


    def _path(
        self,
        document_id: str,
    ) -> Path:

        return (
            self.root
            /
            f"{document_id}.json"
        )


    def save(
        self,
        state: DocumentState,
    ) -> None:


        data = asdict(
            state,
        )


        data["status"] = (
            state.status.value
        )


        self._path(
            state.document_id,
        ).write_text(
            json.dumps(
                data,
                indent=2,
            ),
            encoding="utf-8",
        )


    def load(
        self,
        document_id: str,
    ) -> DocumentState | None:


        path = self._path(
            document_id,
        )


        if not path.exists():

            return None


        data = json.loads(
            path.read_text(
                encoding="utf-8",
            )
        )


        return DocumentState(
            document_id=data["document_id"],
            status=DocumentStatus(
                data["status"]
            ),
            checksum=data.get(
                "checksum"
            ),
            error=data.get(
                "error"
            ),
        )


    def exists(
        self,
        document_id: str,
    ) -> bool:

        return self._path(
            document_id,
        ).exists()
