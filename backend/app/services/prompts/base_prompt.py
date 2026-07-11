class BasePrompt:

    @staticmethod
    def join(*parts) -> str:

        return "\n\n".join(

            part.strip()

            for part in parts

            if part

        )