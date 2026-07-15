from delbot_platform.config.loader import ConfigLoader
from delbot_platform.core.path_manager import PathManager


class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()

        return cls._instance

    def _load(self):
        config_dir = PathManager.CONFIG

        self.settings = ConfigLoader.load(
            config_dir / "settings.yaml"
        )

        self.services = ConfigLoader.load(
            config_dir / "services.yaml"
        )

        self.models = ConfigLoader.load(
            config_dir / "models.yaml"
        )

    def setting(self, key: str):
        return self.settings[key]

    def service(self, name: str):
        return self.services[name]

    def model(self, name: str):
        return self.models[name]