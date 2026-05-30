# backend/test_thesis_search.py

from app.rag.thesis_retriever import (
    search_thesis_dataset
)

results = search_thesis_dataset(
    query="dashboard penerimaan mahasiswa baru",
    top_k=10
)

print("\n====================")
print("SEARCH RESULTS")
print("====================")

for idx, result in enumerate(results):

    print("\n--------------------")

    print(
        f"RESULT {idx + 1}"
    )

    print(
        f"TITLE: {result['title']}"
    )

    print(
        f"SCORE: {result['score']:.4f}"
    )

    print(
        f"YEAR: {result['year']}"
    )

    print(
        f"PRODI: {result['prodi']}"
    )

    print(
        f"URL: {result['url']}"
    )