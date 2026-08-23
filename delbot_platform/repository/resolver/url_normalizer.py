from __future__ import annotations


from urllib.parse import urlparse



class RepositoryURLNormalizer:
    """
    Normalize old DSpace repository URLs.

    Old:
    http://ri.del.ac.id:8080/xmlui/handle/...

    New:
    https://ri.del.ac.id/xmlui/handle/...
    """


    def normalize(
        self,
        url: str,
    ) -> str:


        parsed = urlparse(
            url
        )


        path = parsed.path


        return (
            "https://ri.del.ac.id"
            +
            path
        )