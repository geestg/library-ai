from delbot_platform.research.utils.evidence_extractor import (
    normalize_text
)
from delbot_platform.research.extractors.metadata_extractor import (
    extract_technologies,
    extract_methodologies,
    extract_domains,
    extract_datasets,
    extract_metrics
)


def extract_thesis_evidence(
    thesis: dict
):
    title = thesis.get(
        "title",
        ""
    )
    abstract = thesis.get(
        "abstract",
        ""
    )
    chunk = thesis.get(
        "chunk",
        ""
    )

    # =============================
    # SOURCE BAB WEIGHTING
    # =============================
    # Enriched dataset umumnya menyertakan `source_bab` pada chunk.
    # Kita buat pembobotan berbasis source_bab (bab1/bab3/bab5).
    def _repeat_text(segment: str, weight: int):
        segment = segment or ""
        if not segment.strip() or weight <= 0:
            return ""
        return "\n".join([segment] * weight)

    text_parts = [
        title,
        # abstract bobot sedang
        _repeat_text(abstract, 1),
    ]

    try:
        # chunk kemungkinan besar adalah list of enriched segments
        if isinstance(chunk, list):
            for item in chunk:
                if not isinstance(item, dict):
                    # fallback: anggap item adalah string
                    if isinstance(item, str):
                        text_parts.append(_repeat_text(item, 1))
                    continue

                source_bab = str(item.get("source_bab", "") or "").lower()
                seg_text = item.get("chunk") or item.get("text") or ""
                seg_text = str(seg_text or "")

                if source_bab == "bab5":
                    w = 4
                elif source_bab == "bab3":
                    w = 4
                elif source_bab == "bab1":
                    w = 2
                else:
                    w = 1

                text_parts.append(_repeat_text(seg_text, w))

        elif isinstance(chunk, dict):
            source_bab = str(chunk.get("source_bab", "") or "").lower()
            seg_text = chunk.get("chunk") or chunk.get("text") or ""
            seg_text = str(seg_text or "")

            if source_bab == "bab5":
                w = 4
            elif source_bab == "bab3":
                w = 4
            elif source_bab == "bab1":
                w = 2
            else:
                w = 1

            text_parts.append(_repeat_text(seg_text, w))

        else:
            # fallback: chunk sebagai string biasa
            source_bab = str(thesis.get("source_bab", "") or "").lower()
            if source_bab == "bab5":
                w = 4
            elif source_bab == "bab3":
                w = 4
            elif source_bab == "bab1":
                w = 2
            else:
                w = 1
            text_parts.append(_repeat_text(str(chunk), w))

    except Exception:
        # fallback aman
        source_bab = str(thesis.get("source_bab", "") or "").lower()
        if source_bab == "bab5":
            w = 4
        elif source_bab == "bab3":
            w = 4
        elif source_bab == "bab1":
            w = 2
        else:
            w = 1
        text_parts.append(_repeat_text(str(chunk), w))

    text = normalize_text("\n".join([p for p in text_parts if p]))

    return {
        "technologies":
        extract_technologies(
            text
        ),
        "methodologies":
        extract_methodologies(
            text
        ),
        "domains":
        extract_domains(
            text
        ),
        "datasets":
        extract_datasets(
            text
        ),
        "evaluation_metrics":
        extract_metrics(
            text
        )
    }

