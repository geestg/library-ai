from delbot_platform.gateway.providers.local import LocalProvider


class GatewayService:

    def __init__(self):

        self.provider = LocalProvider()

    async def chat(self, request):

        return await self.provider.chat(request)