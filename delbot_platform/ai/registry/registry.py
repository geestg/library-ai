from __future__ import annotations

from pathlib import Path

from delbot_platform.ai.registry.loader import RegistryLoader
from delbot_platform.ai.registry.model_info import ModelInfo
from delbot_platform.core.path_manager import PathManager


class ModelRegistry:

    def __init__(self) -> None:

        config_file = (
            PathManager.CONFIG
            / "models.yaml"
        )

        self.data = RegistryLoader.load(
            config_file,
        )

    #
    # Internal Helpers
    #

    def _model(
        self,
        category: str,
        name: str,
    ) -> ModelInfo:

        model = self.data[
            category
        ]["models"][name]

        return ModelInfo(
            name=name,
            backend=model["backend"],
            path=str(
                PathManager.ROOT
                / model["path"]
            ),
            port=model["port"],
            dtype=model["dtype"],
            max_context=model["max_context"],
            tensor_parallel_size=model["tensor_parallel_size"],
            gpu_memory_utilization=model["gpu_memory_utilization"],
        )

    def _default_name(
        self,
        category: str,
    ) -> str:

        return self.data[
            category
        ]["default"]

    #
    # Chat
    #

    def chat(
        self,
        name: str,
    ) -> ModelInfo:

        return self._model(
            "chat",
            name,
        )

    def chat_default(
        self,
    ) -> ModelInfo:

        return self.chat(
            self._default_name(
                "chat",
            )
        )

    #
    # Fast Chat
    #

    def fast_chat(
        self,
        name: str,
    ) -> ModelInfo:

        return self._model(
            "fast_chat",
            name,
        )

    def fast_chat_default(
        self,
    ) -> ModelInfo:

        return self.fast_chat(
            self._default_name(
                "fast_chat",
            )
        )

    #
    # Coding
    #

    def coding(
        self,
        name: str,
    ) -> ModelInfo:

        return self._model(
            "coding",
            name,
        )

    def coding_default(
        self,
    ) -> ModelInfo:

        return self.coding(
            self._default_name(
                "coding",
            )
        )

    #
    # Vision
    #

    def vision(
        self,
        name: str,
    ) -> ModelInfo:

        return self._model(
            "vision",
            name,
        )

    def vision_default(
        self,
    ) -> ModelInfo:

        return self.vision(
            self._default_name(
                "vision",
            )
        )

    #
    # Embedding
    #

    def embedding(
        self,
        name: str,
    ) -> ModelInfo:

        return self._model(
            "embedding",
            name,
        )

    def embedding_default(
        self,
    ) -> ModelInfo:

        return self.embedding(
            self._default_name(
                "embedding",
            )
        )

    #
    # Reranker
    #

    def reranker(
        self,
        name: str,
    ) -> ModelInfo:

        return self._model(
            "reranker",
            name,
        )

    def reranker_default(
        self,
    ) -> ModelInfo:

        return self.reranker(
            self._default_name(
                "reranker",
            )
        )

    #
    # OCR
    #

    def ocr(
        self,
        name: str,
    ) -> ModelInfo:

        return self._model(
            "ocr",
            name,
        )

    def ocr_default(
        self,
    ) -> ModelInfo:

        return self.ocr(
            self._default_name(
                "ocr",
            )
        )