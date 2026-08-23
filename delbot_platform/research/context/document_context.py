from __future__ import annotations



class DocumentContextBuilder:



    def build(
        self,
        result
    ):


        context=[]



        for item in result.get(
            "metadata",
            []
        ):


            context.append(
f"""
SOURCE: METADATA

TITLE:
{item.get("title")}

YEAR:
{item.get("year")}

ABSTRACT:
{item.get("abstract")}
"""
            )



        for item in result.get(
            "pdf",
            []
        ):


            context.append(
f"""
SOURCE: PDF

PAGE:
{item.get("page")}

CONTENT:
{item.get("text")}
"""
            )



        return "\n\n".join(context)
