from enum import Enum


class PipelineAction(str, Enum):

    CONTINUE = "continue"

    STOP = "stop"

    SKIP = "skip"
