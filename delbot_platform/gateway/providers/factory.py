from __future__ import annotations

from delbot_platform.ai.registry.model_backend import (
    ModelBackend,
)
from delbot_platform.gateway.providers.base import (
    BaseProvider,
)
from delbot_platform.gateway.providers.infinity import (
    InfinityProvider,
)
from delbot_platform.gateway.providers.local import (
    LocalProvider,
)
from delbot_platform.gateway.providers.vllm import (
    VLLMProvider,
)


class ProviderFactory:

    @staticmethod
    def build(
        backend: ModelBackend,
    ) -> BaseProvider:

        if backend is ModelBackend.VLLM:

            return VLLMProvider()

        if backend is ModelBackend.INFINITY:

            return InfinityProvider()

        if backend is ModelBackend.NATIVE:

            #
            # NativeProvider akan diimplementasikan
            # pada sprint berikutnya.
            #

            return LocalProvider()

        raise ValueError(
            f"Unsupported backend: {backend}"
        )