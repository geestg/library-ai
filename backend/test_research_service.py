from app.services.research_service import (
    research_analysis
)

result = research_analysis(

    query="dashboard penerimaan mahasiswa baru",

    top_k=5
)

print("\n====================")
print("RESEARCH ANALYSIS")
print("====================\n")

print(
    result["analysis"]
)