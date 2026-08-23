from __future__ import annotations

import json
import sys

import fitz


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage:")
        print("python inspect_pymupdf_span.py file.pdf")
        raise SystemExit(1)

    document = fitz.open(sys.argv[1])

    page = document[0]

    layout = page.get_text(
        "dict",
    )

    for block in layout.get("blocks", []):

        for line in block.get("lines", []):

            for span in line.get("spans", []):

                print(
                    json.dumps(
                        span,
                        indent=4,
                        ensure_ascii=False,
                        default=str,
                    )
                )

                return

    document.close()


if __name__ == "__main__":
    main()
