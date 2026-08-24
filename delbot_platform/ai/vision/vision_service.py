from __future__ import annotations

from typing import Optional, Dict, Any, List

from delbot_platform.core.config import settings
from delbot_platform.orchestration.model_selector import select_model
from delbot_platform.ai.llm.model_gateway import gateway
from delbot_platform.ai.vision.vision_image_utils import normalize_image_base64


from delbot_platform.research.retrieval.embedder import get_embedding
from delbot_platform.research.retrieval.qdrant_client import client
from delbot_platform.research.retrieval.bm25_engine import bm25_search

from delbot_platform.core.constants import (
    THESIS_DATASET_COLLECTION,
    USER_DOCUMENT_COLLECTION,
    RESEARCH_PAPER_COLLECTION,
)

from delbot_platform.research.retrieval.context_synthesizer import build_citation_context


# All collections for general AI knowledge
ALL_COLLECTIONS = [
    USER_DOCUMENT_COLLECTION,
    THESIS_DATASET_COLLECTION,
    RESEARCH_PAPER_COLLECTION,
]


def _build_multimodal_prompt(
    prompt: str,
    rag_context: Optional[str] = None
) -> str:
    parts = [
        "Anda adalah DELBot yang menjawab berdasarkan gambar dan konteks pengetahuan.",
    ]
    if rag_context:
        parts.append("\n[KONTEKS PENGETAHUAN YANG RELEVAN]")
        parts.append(rag_context)
    parts.extend([
        "\n[PERTANYAAN]",
        prompt,
    ])
    return "\n".join(parts)


def _search_collection(collection: str, query: str, limit: int = 10) -> List[Dict]:
    try:
        embedding = get_embedding(query)
        response = client.query_points(
            collection_name=collection,
            query=embedding,
            limit=limit,
            with_payload=True
        )
        results = []
        for point in response.points:
            results.append({
                "payload": point.payload,
                "score": float(point.score),
                "source": collection
            })
        return results
    except Exception:
        return []


def _general_rag_search(query: str, limit: int = 5) -> List[Dict]:
    """Search across ALL collections (user_documents, thesis, research_papers)"""
    all_results = []
    for collection in ALL_COLLECTIONS:
        results = _search_collection(collection, query, limit=15)
        all_results.extend(results)
    # Sort by score and deduplicate
    seen = set()
    unique_results = []
    for item in sorted(all_results, key=lambda x: x["score"], reverse=True):
        doc_id = item["payload"].get("url") or item["payload"].get("title")
        if doc_id and doc_id not in seen:
            seen.add(doc_id)
            unique_results.append(item)
    return unique_results[:limit]


import base64
import io
from PIL import Image


def _extract_text_via_ocr(image_base64: Optional[str] = None, image_url: Optional[str] = None) -> str:
    try:
        import pytesseract
        image = None
        if image_base64:
            clean_b64 = image_base64
            if "," in clean_b64:
                clean_b64 = clean_b64.split(",", 1)[1]
            img_bytes = base64.b64decode(clean_b64)
            image = Image.open(io.BytesIO(img_bytes))
        elif image_url and not image_url.startswith("http"):
            image = Image.open(image_url)
        
        if image:
            if image.mode not in ("L", "RGB"):
                image = image.convert("RGB")
            text = pytesseract.image_to_string(image)
            return text.strip()
    except Exception as e:
        print(f"[OCR EXTRACTION] {e}")
    return ""


def vision_chat(
    *,
    prompt: str,
    image_base64: Optional[str] = None,
    image_url: Optional[str] = None,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    enable_rag: bool = True,
    rag_limit: int = 5,
    max_tokens: int = 1024,
) -> Dict[str, Any]:
    if not image_base64 and not image_url:
        raise ValueError("Harus mengirim salah satu: image_base64 atau image_url")

    vision_defaults = select_model("multimodal")

    model = model or vision_defaults["model"]
    provider = provider or vision_defaults["provider"]

    if image_base64:
        image_ref = normalize_image_base64(image_base64)
    else:
        image_ref = image_url

    rag_context = None
    rag_results = []
    if enable_rag:
        rag_results = _general_rag_search(query=prompt, limit=rag_limit)
        if rag_results:
            rag_context = build_citation_context(rag_results)

    # 1. Extract text from image via OCR (allows pure-text LLMs like Qwen3-30B-MoE to understand image content)
    ocr_text = _extract_text_via_ocr(image_base64=image_base64, image_url=image_url)

    if ocr_text:
        print(f"[VISION SERVICE] OCR extracted {len(ocr_text)} chars from image. Routing to LLM as multimodal prompt.")
        multimodal_prompt = f"""Anda adalah DELBot, asisten cerdas Perpustakaan dan Riset IT Del.
Pengguna telah mengunggah gambar/tangkapan layar dengan isi teks yang berhasil dibaca sebagai berikut:
========================================
{ocr_text}
========================================

Pertanyaan / Instruksi Pengguna:
{prompt}

Tolong jawab dan analisis pertanyaan pengguna secara lengkap, jelas, dan ramah berdasarkan isi gambar di atas."""
        image_to_send = None
    else:
        multimodal_prompt = _build_multimodal_prompt(prompt, rag_context)
        image_to_send = image_ref

    response = gateway.generate_response(
        prompt=multimodal_prompt,
        model=model,
        provider=provider,
        image_ref=image_to_send,
        max_tokens=max_tokens,
    )

    return {
        "status": "success",
        "provider": provider,
        "model": model,
        "response": response,
        "ocr_detected": bool(ocr_text),
        "rag_enabled": enable_rag,
        "rag_sources_count": len(rag_results),
        "rag_sources": rag_results[:3] if rag_results else [],
        "search_collections": ALL_COLLECTIONS if enable_rag else [],
    }
