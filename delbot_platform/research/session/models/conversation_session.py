from dataclasses import dataclass, field

MAX_HISTORY = 10


# =====================================
# CONVERSATION MESSAGE
# =====================================

@dataclass
class ConversationMessage:

    role: str

    content: str

    citations: list = field(default_factory=list)

    sources: list = field(default_factory=list)


# =====================================
# CONVERSATION SESSION
# =====================================

@dataclass
class ConversationSession:

    messages: list[ConversationMessage] = field(
        default_factory=list
    )

    # =====================================
    # APPEND MESSAGE
    # =====================================

    def append(
        self,
        role: str,
        content: str,
        citations: list | None = None,
        sources: list | None = None,
    ):

        self.messages.append(

            ConversationMessage(

                role=role,

                content=content,

                citations=citations or [],

                sources=sources or [],

            )

        )

        # Keep only latest history
        self.messages = self.messages[
            -MAX_HISTORY:
        ]

    # =====================================
    # LEGACY COMPATIBILITY
    # =====================================

    def add_message(
        self,
        role: str,
        content: str,
    ):
        """
        Compatibility wrapper.

        Deprecated.
        Use append() instead.
        """

        self.append(
            role=role,
            content=content,
        )

    # =====================================
    # BUILD HISTORY
    # =====================================

    def build_history(self) -> str:

        return "\n".join(

            [

                f"{message.role}: {message.content}"

                for message in self.messages

            ]

        )

    # =====================================
    # GET LAST MESSAGE
    # =====================================

    def last_message(self):

        if not self.messages:

            return None

        return self.messages[-1]

    # =====================================
    # GET LAST USER MESSAGE
    # =====================================

    def last_user_message(self):

        for message in reversed(self.messages):

            if message.role == "user":

                return message

        return None

    # =====================================
    # GET LAST ASSISTANT MESSAGE
    # =====================================

    def last_assistant_message(self):

        for message in reversed(self.messages):

            if message.role == "assistant":

                return message

        return None

    # =====================================
    # TOTAL MESSAGE
    # =====================================

    def total_messages(self) -> int:

        return len(self.messages)

    # =====================================
    # CLEAR
    # =====================================

    def clear(self):

        self.messages.clear()

    # =====================================
    # EXPORT
    # =====================================

    def export(self) -> list[dict]:
        return [
            {
                "role": message.role,
                "content": message.content,
                "citations": getattr(message, "citations", []) or [],
                "sources": getattr(message, "sources", []) or [],
            }
            for message in self.messages
        ]

    # =====================================
    # SERIALIZE
    # =====================================

    def to_dict(self):

        return {

            "messages": [

                {

                    "role": message.role,

                    "content": message.content,

                    "citations": getattr(message, "citations", []) or [],

                    "sources": getattr(message, "sources", []) or [],

                }

                for message in self.messages

            ],

            "total_messages": len(
                self.messages
            ),

        }