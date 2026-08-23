from __future__ import annotations


from urllib.parse import urljoin

import httpx

from bs4 import BeautifulSoup



class DSpaceHTMLResolver:
    """
    Resolve PDF URL from DSpace item HTML page.

    Strategy:

    1. Open item page
    2. Parse anchor links
    3. Find PDF attachment
    """


    def __init__(
        self,
        timeout: float = 30.0,
    ) -> None:


        self.client = httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            headers={
                "User-Agent":
                (
                    "Mozilla/5.0 "
                    "DELBot Repository Resolver"
                )
            }
        )



    def resolve(
        self,
        repository_url: str,
    ) -> str | None:


        response = self.client.get(
            repository_url
        )


        print(
            "[STATUS]",
            response.status_code
        )


        if response.status_code != 200:

            return None



        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )


        links = soup.find_all(
            "a"
        )


        for link in links:


            href = link.get(
                "href"
            )


            if not href:

                continue



            text = (
                link.text
                .strip()
                .lower()
            )


            url = urljoin(
                repository_url,
                href,
            )


            if (
                ".pdf" in url.lower()
                or
                ".pdf" in text
            ):

                print(
                    "[FOUND]",
                    url
                )

                return url



        return None
