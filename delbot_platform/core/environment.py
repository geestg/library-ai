import os

from delbot_platform.core.path_manager import PathManager


class EnvironmentManager:

    @classmethod
    def setup(cls):

        env = {

            "HF_HOME":
                str(PathManager.ROOT / "cache" / "huggingface"),

            "TRANSFORMERS_CACHE":
                str(PathManager.ROOT / "cache" / "transformers"),

            "TORCH_HOME":
                str(PathManager.ROOT / "cache" / "torch"),

            "MODEL_HOME":
                str(PathManager.ROOT / "models"),

            "TMPDIR":
                str(PathManager.RUNTIME / "tmp"),

            "TOKENIZERS_PARALLELISM":
                "false",

            "CUDA_HOME":
                "/usr/local/cuda",

        }

        for key, value in env.items():

            os.environ[key] = value

        return env