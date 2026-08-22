import sys
sys.path.insert(0, r'd:\DEL\library-ai\backend')

from app.orchestration.intent_classifier import classify_intent
from app.services.research.models.research_models import ResearchContext
from app.services.research.search_engine import run_search

query = "Saya butuh ide skripsi bertema optimasi klasifikasi citra medis dengan deep learning untuk prodi informatika"

print("=========================================", flush=True)
print("DIAGNOSIS PIPELINE UNTUK QUERI USER", flush=True)
print("=========================================", flush=True)

intent = classify_intent(query)
print(f"1. Classified Intent: '{intent}'", flush=True)

ctx = ResearchContext(query=query, requested_prodi="informatika")
print("\n2. Executing run_search(ctx)...", flush=True)
ctx = run_search(ctx)

print(f"\n   - theses count: {len(ctx.theses)}", flush=True)
print(f"   - citations count: {len(ctx.citations)}", flush=True)
for idx, c in enumerate(ctx.citations, 1):
    print(f"     [{idx}] ID: {c.get('source_id')} | Title: {c.get('title')} | Prodi: {c.get('prodi')}", flush=True)

print("\n=========================================", flush=True)
