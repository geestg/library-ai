from __future__ import annotations


from uuid import uuid5, NAMESPACE_DNS


from qdrant_client.models import (
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)


from delbot_platform.vectors import (
    VectorRecord,
)

from delbot_platform.vectorstore.qdrant.singleton import (
    get_qdrant_store,
)



class QdrantRepository:


    def __init__(
        self,
        store=None,
    ) -> None:


        self.store = (

            store

            if store is not None

            else get_qdrant_store()

        )


        self.store.create_collection()



    def delete_document(
        self,
        document_id: str,
    ) -> None:


        self.store.client.delete(

            collection_name=self.store.collection,

            points_selector=Filter(

                must=[

                    FieldCondition(

                        key="document_id",

                        match=MatchValue(

                            value=document_id

                        ),

                    )

                ]

            )

        )



    def save(
        self,
        vectors: list[VectorRecord],
    ) -> int:


        if not vectors:

            return 0



        document_id = (

            vectors[0]
            .metadata
            .get(
                "document_id"
            )

        )


        if document_id:

            self.delete_document(
                document_id
            )



        points = []



        for vector in vectors:


            point_id = str(

                uuid5(

                    NAMESPACE_DNS,

                    vector.id,

                )

            )


            points.append(

                PointStruct(

                    id=point_id,

                    vector=vector.vector,

                    payload=vector.metadata,

                )

            )



        self.store.client.upsert(

            collection_name=self.store.collection,

            points=points,

        )


        return len(points)



    def count(
        self,
    ) -> int:


        result = (

            self.store.client
            .count(
                collection_name=self.store.collection,
            )

        )


        return result.count