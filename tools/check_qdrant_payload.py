from qdrant_client import QdrantClient


client=QdrantClient(
    host="127.0.0.1",
    port=6333
)



points,_=client.scroll(
    collection_name="delbot_documents",
    limit=10
)



for p in points:

    print("===================")

    print(
        "ID:",
        p.id
    )

    print(
        p.payload.keys()
    )

    print(
        p.payload
    )
