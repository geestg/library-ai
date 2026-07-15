from pathlib import Path

import yaml


class ConfigLoader:

    @staticmethod
    def load(path: Path):

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:

            return yaml.safe_load(f)