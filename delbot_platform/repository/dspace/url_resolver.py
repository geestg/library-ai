from __future__ import annotations


from urllib.parse import urljoin



class DSpaceURLResolver:
    """
    Resolve DSpace artifact URLs.

    Converts legacy DSpace URLs:

        http://host:8080/xmlui/...

    into public URLs:

        https://host/...

    """


    def resolve(
        self,
        url: str,
    ) -> str:


        if not url:

            raise ValueError(
                "Empty DSpace URL"
            )


        #
        # Legacy DSpace
        #

        if ":8080" in url:

            url = (
                url
                .replace(
                    "http://",
                    "https://",
                )
                .replace(
                    ":8080",
                    "",
                )
            )


        #
        # xmlui path normalization
        #

        if "/xmlui/" in url:

            url = url.replace(
                "/xmlui/",
                "/",
            )


        return url
