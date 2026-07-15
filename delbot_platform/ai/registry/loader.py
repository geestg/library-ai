from pathlib import Path

import yaml


class RegistryLoader:

    @staticmethod
    def load(file: Path):

        with open(
            file,
            "r",
            encoding="utf-8",
        ) as f:

            return yaml.safe_load(f)