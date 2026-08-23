from __future__ import annotations


from pathlib import Path


import httpx



class PDFDownloader:



    def download(
        self,
        url: str,
        destination: Path,
    ) -> Path:


        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


        with httpx.stream(
            "GET",
            url,
            timeout=120,
            follow_redirects=True,
        ) as response:


            response.raise_for_status()


            with destination.open(
                "wb"
            ) as file:


                for chunk in response.iter_bytes():

                    file.write(
                        chunk
                    )


        return destination

