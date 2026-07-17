from __future__ import annotations


from pathlib import Path


import httpx


from delbot_platform.repository.ingestion import (
    FileDownloader,
)


from delbot_platform.repository.models import (
    RepositoryItem,
)


from delbot_platform.repository.dspace.url_resolver import (
    DSpaceURLResolver,
)



class DSpaceDownloader(
    FileDownloader,
):


    def __init__(
        self,
        resolver: DSpaceURLResolver | None = None,
    ) -> None:


        self.resolver = (
            resolver
            if resolver is not None
            else DSpaceURLResolver()
        )



    def download(
        self,
        item: RepositoryItem,
        destination: Path,
    ) -> Path:


        if item.source_url is None:

            raise ValueError(
                f"Missing source URL: {item.id}"
            )


        destination.mkdir(
            parents=True,
            exist_ok=True,
        )


        url = self.resolver.resolve(
            item.source_url,
        )


        filename = (
            Path(url).name
            or "document.pdf"
        )


        pdf = (
            destination
            /
            filename
        )


        with httpx.stream(
            "GET",
            url,
            timeout=120,
            follow_redirects=True,
        ) as response:


            response.raise_for_status()


            with pdf.open(
                "wb"
            ) as file:


                for chunk in response.iter_bytes():

                    file.write(
                        chunk
                    )


        return pdf