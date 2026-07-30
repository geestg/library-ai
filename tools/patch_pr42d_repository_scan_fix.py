from pathlib import Path
import re
import ast
import py_compile

ROOT = Path(__file__).resolve().parents[1]

candidate_files = [
    ROOT / "delbot_platform/repository/repository_service.py",
    ROOT / "delbot_platform/repository/service.py",
    ROOT / "delbot_platform/repository/services.py",
    ROOT / "delbot_platform/repository/scan_service.py",
]

target = None

for f in candidate_files:
    if f.exists():
        target = f
        break

if target is None:
    for f in ROOT.rglob("*.py"):
        try:
            txt = f.read_text(encoding="utf-8")
        except Exception:
            continue

        if (
            "RepositoryScanResult" in txt
            and "RepositoryItem" in txt
            and "pdf_available" in txt
        ):
            target = f
            break

if target is None:
    raise SystemExit("Repository service not found.")

text = target.read_text(encoding="utf-8")

if "from pathlib import Path" not in text:
    if "from pathlib import Path" not in text:
        text = "from pathlib import Path\n" + text

if "pdf_root = Path(" not in text:

    pattern = r"status\s*=\s*RepositoryStatus\.METADATA_ONLY"

    replacement = """
pdf_root = Path(__file__).resolve().parents[2] / "repository_data" / "pdf"

pdf_file = pdf_root / f"{item.id}.pdf"

if pdf_file.exists():
    item.local_path = str(pdf_file)
    item.status = RepositoryStatus.PDF_AVAILABLE
else:
    item.status = RepositoryStatus.METADATA_ONLY
"""

    text = re.sub(
        pattern,
        replacement,
        text,
        count=1,
        flags=re.MULTILINE,
    )

text = re.sub(
    r'pdf_available\s*=\s*0',
    'pdf_available=sum(1 for x in items if x.status == RepositoryStatus.PDF_AVAILABLE)',
    text,
)

text = re.sub(
    r'pdf_missing\s*=\s*len\(items\)',
    'pdf_missing=sum(1 for x in items if x.status != RepositoryStatus.PDF_AVAILABLE)',
    text,
)

target.write_text(text, encoding="utf-8")

ast.parse(text)
py_compile.compile(str(target), doraise=True)

print("PATCH :", target.relative_to(ROOT))
print("AST PASS")
print("COMPILE PASS")
