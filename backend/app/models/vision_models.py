from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, model_validator


class VisionChatRequest(BaseModel):
    prompt: str
    image_base64: Optional[str] = None
    image_url: Optional[str] = None

    @model_validator(mode="after")
    def validate_image_reference(self):
        if not self.image_base64 and not self.image_url:
            raise ValueError("Harus mengirim salah satu: image_base64 atau image_url")
        return self
