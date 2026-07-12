from enum import Enum


class PromptType(
    str,
    Enum,
):

    ANSWER = "answer"

    DOCUMENT = "document"

    VERIFIER = "verifier"

    QUERY_RESOLUTION = "query_resolution"

    RESEARCH = "research"

    CREATIVE = "creative"

    TITLE = "title"