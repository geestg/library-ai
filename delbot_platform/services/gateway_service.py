from __future__ import annotations

from delbot_platform.launcher.gateway_launcher import GatewayLauncher
from delbot_platform.services.service import PlatformService


class GatewayService(PlatformService):

    @property
    def name(self) -> str:
        return "gateway"

    @property
    def host(self) -> str:
        return "127.0.0.1"

    @property
    def port(self) -> int:
        return 8100

    @property
    def enabled(self) -> bool:
        return True

    def launcher(self):
        return GatewayLauncher()

    def launch_spec(self):
        return self.launcher().build()

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def restart(self):
        raise NotImplementedError

    def health(self):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError
