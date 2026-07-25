from __future__ import annotations

from delbot_platform.vectorstore.qdrant.singleton import (
    get_qdrant_store,
)


class SourceIndex:

    def __init__(
        self,
    ) -> None:

        self.store = get_qdrant_store()
        self.store.create_collection()

    def build(
        self,
    ):

        sources = {}

        offset = None

        while True:

            points, offset = self.store.scroll(
                limit=100,
                offset=offset,
            )

            for point in points:

                payload = point.payload or {}

                source = payload.get(
                    "source",
                )

                if not source:
                    continue

                if source not in sources:

                    sources[source] = {
                        "pages": 0,
                        "sample": "",
                    }

                sources[source]["pages"] += 1

                if not sources[source]["sample"]:

                    sources[source]["sample"] = (
                        payload.get(
                            "text",
                            "",
                        )[:500]
                    )

            if offset is None:
                break

        return sources
