from __future__ import annotations


from urllib.parse import urljoin


import httpx

from bs4 import BeautifulSoup


from .base import RepositoryProvider



class DSpaceProvider(
    RepositoryProvider
):


    def resolve_pdf(
        self,
        url: str,
    ) -> str | None:


        try:

            response = httpx.get(

                url,

                timeout=20,

                follow_redirects=True,

                headers={
                    "User-Agent":
                    "Mozilla/5.0 DELBot"
                }

            )


        except Exception:

            return None



        if response.status_code != 200:

            return None



        soup = BeautifulSoup(

            response.text,

            "html.parser"

        )


        for link in soup.find_all(
            "a"
        ):


            href = link.get(
                "href"
            )


            if not href:

                continue



            text = (
                link
                .get_text(
                    " ",
                    strip=True
                )
                .lower()
            )



            if (

                ".pdf" in href.lower()

                or

                "fulltext" in text

                or

                "view/open" in text

            ):


                return urljoin(

                    url,

                    href

                )


        return None