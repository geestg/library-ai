from app.services.research.prodi.prodi_profiles import (
    PRODI_PROFILES
)


def build_prodi_analysis(

    domain: str,

    competency_analysis: dict
):

    profile = PRODI_PROFILES.get(
        domain
    )

    if not profile:

        return {

            "prodi": domain,

            "focus_areas": [],

            "dominant_competencies": [],

            "research_alignment": 0.0
        }

    competencies = [

        item["name"]

        for item

        in competency_analysis.get(
            "competencies",
            []
        )
    ]

    expected = set(

        profile.get(
            "expected_competencies",
            []
        )
    )

    matched = [

        competency

        for competency

        in competencies

        if competency in expected
    ]

    alignment = 0.0

    if expected:

        alignment = round(

            len(matched)

            /

            len(expected),

            2
        )

    return {

        "prodi": domain,

        "focus_areas":

        profile.get(
            "focus_areas",
            []
        ),

        "dominant_competencies":

        competencies[:10],

        "matched_competencies":

        matched,

        "research_alignment":

        alignment
    }