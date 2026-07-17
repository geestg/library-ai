from __future__ import annotations

from dataclasses import dataclass
from enum import Enum



class DocumentStatus(
    Enum,
):

    DISCOVERED = "discovered"

    DOWNLOADING = "downloading"

    DOWNLOADED = "downloaded"

    PROCESSING = "processing"

    PROCESSED = "processed"

    FAILED = "failed"



@dataclass(slots=True, frozen=True)
class DocumentState:
    """
    Persistent state for one repository document.
    """


    document_id: str

    status: DocumentStatus

    checksum: str | None = None

    error: str | None = None

