from __future__ import annotations


def normalize_image_base64(image_base64: str) -> str:
    """Return a data-URL string for a base64-encoded image.

    The vision flow accepts either a full data URL or raw base64 payload.
    """

    value = image_base64.strip()

    if not value:
        raise ValueError("image_base64 cannot be empty")

    if value.startswith("data:image/"):
        return value

    if "," in value and value.split(",", 1)[0].startswith("data:image/"):
        return value

    return f"data:image/png;base64,{value}"