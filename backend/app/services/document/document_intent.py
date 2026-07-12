# =====================================
# DOCUMENT INTENT DETECTOR
# =====================================

def detect_document_intent(
    query: str
):

    q = query.lower()

    # =================================
    # SUMMARY
    # =================================

    if any(

        keyword in q

        for keyword in [

            "ringkas",

            "summary",

            "summarize",

            "ringkasan",

            "jelaskan isi"

        ]

    ):

        return "summary"

    # =================================
    # TIMELINE
    # =================================

    if any(

        keyword in q

        for keyword in [

            "timeline",

            "jadwal",

            "tanggal",

            "deadline",

            "kapan"

        ]

    ):

        return "timeline"

    # =================================
    # REQUIREMENTS
    # =================================

    if any(

        keyword in q

        for keyword in [

            "syarat",

            "ketentuan",

            "persyaratan",

            "requirement"

        ]

    ):

        return "requirements"

    # =================================
    # CHECKLIST
    # =================================

    if any(

        keyword in q

        for keyword in [

            "checklist",

            "todo",

            "yang harus disiapkan",

            "apa saja yang perlu"

        ]

    ):

        return "checklist"

    # =================================
    # DELIVERABLE
    # =================================

    if any(

        keyword in q

        for keyword in [

            "deliverable",

            "submission",

            "yang harus dikumpulkan",

            "yang dikumpulkan"

        ]

    ):

        return "deliverables"

    # =================================
    # QA
    # =================================

    return "qa"

