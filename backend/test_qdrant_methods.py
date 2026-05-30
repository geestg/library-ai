from app.rag.qdrant_client import client

print("CLIENT TYPE:")
print(type(client))

print("\nAVAILABLE METHODS:")

for method in dir(client):

    if (
        "search" in method.lower()
        or "query" in method.lower()
        or "point" in method.lower()
    ):

        print(method)