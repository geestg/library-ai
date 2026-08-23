from __future__ import annotations



class ContextBuilder:


    def build(
        self,
        results
    ):


        contexts=[]


        for index,item in enumerate(results):


            text=item.get(
                "text",
                ""
            )


            source=item.get(
                "source",
                ""
            )


            page=item.get(
                "page",
                ""
            )


            contexts.append(
                f"""
SOURCE {index+1}

FILE:
{source}

PAGE:
{page}

CONTENT:
{text}
"""
            )


        return "\n\n".join(
            contexts
        )
