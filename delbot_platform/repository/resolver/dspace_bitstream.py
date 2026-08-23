from __future__ import annotations


from urllib.parse import urlparse


import httpx



class DSpaceBitstreamResolver:
    """
    Resolve DSpace PDF directly from bitstream URL.

    Does not scrape HTML.
    Uses known DSpace pattern.
    """


    FILE_NAMES = [

        "Fulltext.pdf",

        "fulltext.pdf",

        "FullText.pdf",

        "fulltext",

        "thesis.pdf",

        "document.pdf",

    ]


    def __init__(
        self,
        timeout: float = 15.0,
    ) -> None:


        self.client = httpx.Client(

            timeout=timeout,

            follow_redirects=True,

        )



    def resolve(
        self,
        repository_url: str,
    ) -> str | None:


        parsed = urlparse(
            repository_url
        )


        path = parsed.path


        if "/handle/" not in path:

            return None



        handle = path.split(
            "/handle/"
        )[1]



        base = (
            f"https://{parsed.hostname}"
            "/bitstream/handle/"
            f"{handle}"
        )



        for filename in self.FILE_NAMES:


            candidate = (
                f"{base}/{filename}"
            )


            try:


                response = self.client.head(
                    candidate,
                )


                print(
                    "[CHECK]",
                    candidate,
                    response.status_code,
                )


                if response.status_code == 200:

                    content_type = (
                        response.headers.get(
                            "content-type",
                            "",
                        )
                    )


                    if "pdf" in content_type.lower():

                        return candidate



            except Exception:

                continue



        return None
