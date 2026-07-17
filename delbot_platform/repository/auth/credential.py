from __future__ import annotations


from dataclasses import dataclass



@dataclass(slots=True, frozen=True)
class RepositoryCredential:
    """
    Repository authentication credential.

    Stored separately from repository metadata.
    """

    username: str

    password: str

    repository_id: str
