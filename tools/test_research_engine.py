from __future__ import annotations


import sys

from pathlib import Path



ROOT=Path(__file__).resolve().parent.parent


sys.path.insert(

    0,

    str(ROOT)

)



from delbot_platform.research.research_engine import ResearchEngine




engine=ResearchEngine()



result=engine.ask(

    "Bagaimana metodologi penelitian machine learning?"

)



print("="*60)

print(result["answer"])


print("="*60)

print("CITATIONS")


for c in result["citations"]:

    print(c)
