from collections import Counter


PRODI_TO_DOMAIN = {

    "Informatika":
        "informatika",

    "Sistem Informasi":
        "sistem_informasi",

    "Teknik Elektro":
        "teknik_elektro",

    "Teknik Bioproses":
        "bioproses",

    "Manajemen Rekayasa":
        "manajemen_rekayasa",

    "Teknik Metalurgi":
        "metalurgi",

    "Teknologi Informasi":
        "teknologi_informasi",

    "Teknologi Komputer":
        "teknologi_komputer",

    "Teknologi Rekayasa Perangkat Lunak":
        "trpl"
}


def resolve_domain(
    query_domain: dict,
    theses: list
):

    # =====================================
    # FALLBACK
    # =====================================

    if not theses:

        return {

            **query_domain,

            "source":
                "query"
        }

    # =====================================
    # COUNT PRODI
    # =====================================

    counter = Counter()

    for thesis in theses:

        prodi = (

            thesis.get(
                "prodi",
                ""
            )
            or ""
        ).strip()

        mapped = PRODI_TO_DOMAIN.get(
            prodi
        )

        if mapped:

            counter[mapped] += 1

    # =====================================
    # NO PRODI FOUND
    # =====================================

    if len(counter) == 0:

        return {

            **query_domain,

            "source":
                "query"
        }

    # =====================================
    # DOMINANT DOMAIN
    # =====================================

    dominant_domain = (

        counter.most_common(
            1
        )[0][0]
    )

    confidence = round(

        counter[
            dominant_domain
        ] / max(
            len(theses),
            1
        ),

        2
    )

    return {

        "domain":
            dominant_domain,

        "confidence":
            confidence,

        "source":
            "retrieval"
    }
