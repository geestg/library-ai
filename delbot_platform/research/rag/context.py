from __future__ import annotations



class ResearchContextBuilder:


    def build(
        self,
        documents:list,
    ):


        context=[]


        for doc in documents:

            payload = doc.get(
                "payload",
                {}
            )


            text = payload.get(
                "text",
                ""
            )


            context.append(
                text
            )


        return "\n\n".join(
            context
        )
