from typing import Dict


# =====================================
# EXTRACT THESIS METADATA
# =====================================

def extract_metadata(data: Dict):

    return {

        # =============================
        # BASIC INFO
        # =============================

        "title": data.get(
            "title",
            ""
        ),

        "author": data.get(
            "author",
            ""
        ),

        "year": data.get(
            "year",
            ""
        ),

        # =============================
        # ACADEMIC INFO
        # =============================

        "prodi": data.get(
            "prodi",
            ""
        ),

        "method": data.get(
            "method",
            ""
        ),

        "keywords": data.get(
            "keywords",
            []
        ),

        # =============================
        # CONTENT
        # =============================

        "abstract": data.get(
            "abstract",
            ""
        ),

        # =============================
        # SOURCE
        # =============================

        "url": data.get(
            "url",
            ""
        ),
    }