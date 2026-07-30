from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

file = ROOT / "delbot_platform/research/pipeline/research_answer_pipeline.py"

code = file.read_text()

code = code.replace(
    "def answer(",
    "async def answer(",
)

code = code.replace(
    "rag = self.rag.build(",
    "rag = await self.rag.build(",
)

file.write_text(code)

print("PATCHED")
print(file)
