import json
from delbot_platform.research.research_engine import research_analysis

def run_test():
    query = "mencari ide skripsi tentang machine learning untuk klasifikasi citra"
    print("=" * 60)
    print(f"TESTING RESEARCH AGENT PIPELINE")
    print(f"Query: {query}")
    print("=" * 60)
    
    try:
        response = research_analysis(
            query=query,
            session_id="test_session_123",
            top_k=10,
            mode="analysis"
        )
        
        print("\n[SUCCESS] Response generated successfully!")
        print("-" * 60)
        print("Generated Analysis Output:")
        print("-" * 60)
        print(response.get("analysis", "No analysis content found!"))
        
        print("\n" + "=" * 60)
        print("Detailed Metrics and Extracted Metadata:")
        print("=" * 60)
        
        profile = response.get("research_profile", {})
        
        # Prodi Alignments
        prodi_info = profile.get("prodi", {})
        print(f"Primary Prodi: {prodi_info.get('prodi')}")
        print(f"Alignment Score: {prodi_info.get('research_alignment')}")
        print(f"All Prodi Alignments: {prodi_info.get('prodi_alignments')}")
        
        # Novelty Analysis
        novelty_info = profile.get("novelty", {})
        print(f"Novelty Score: {novelty_info.get('novelty_score')}")
        print(f"Novelty Level: {novelty_info.get('novelty_level')}")
        print(f"Reasons: {novelty_info.get('reasons')}")
        
        # Extracted Bab 5 Gaps
        gap_info = profile.get("gap", {})
        bab5_gaps = gap_info.get("bab5_gaps", [])
        print(f"Extracted Bab 5 suggestion sentences count: {len(bab5_gaps)}")
        if bab5_gaps:
            print("Sample Bab 5 Gap sentence:")
            print(f" - {bab5_gaps[0].get('sentence')} (from '{bab5_gaps[0].get('title')}')")
            
    except Exception as e:
        print(f"\n[ERROR] Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
