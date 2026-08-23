from collections import Counter
from typing import List, Dict


# =====================================
# EXTRACT THEMES
# =====================================

def extract_themes(documents):

    keywords = []

    for doc in documents:

        payload = doc.get("payload", {})

        text = f"""
        {payload.get("title", "")}
        {payload.get("abstract", "")}
        """.lower()

        important_terms = [

            "cnn",
            "svm",
            "transformer",
            "deep learning",
            "machine learning",
            "classification",
            "sentiment",
            "nlp",
            "computer vision",
            "resnet",
            "mobilenet",
            "lstm",
            "bert",
            "tf-idf",
            "augmentation",
            "transfer learning"
        ]

        for term in important_terms:

            if term in text:

                keywords.append(term)

    counter = Counter(keywords)

    return counter.most_common(10)


# =====================================
# SYNTHESIZE CONTEXT
# =====================================

def synthesize_context(documents):

    synthesized = []

    themes = extract_themes(documents)

    # =================================
    # THEMES
    # =================================

    if themes:

        synthesized.append(
            "Tema dominan penelitian:"
        )

        for term, count in themes:

            synthesized.append(
                f"- {term} ({count} penelitian)"
            )

    # =================================
    # DOCUMENT INSIGHTS
    # =================================

    synthesized.append(
        "\nInsight penting dari penelitian:"
    )

    for idx, doc in enumerate(documents[:5]):

        payload = doc.get("payload", {})

        title = payload.get(
            "title",
            ""
        )

        abstract = payload.get(
            "abstract",
            ""
        )

        short_abstract = abstract[:500]

        synthesized.append(f"""

Penelitian {idx + 1}:
Judul:
{title}

Insight:
{short_abstract}

""")

    # =================================
    # RESEARCH OPPORTUNITY
    # =================================

    synthesized.append("""

Potensi arah penelitian lanjutan:
- optimasi model
- hybrid AI architecture
- explainable AI
- multimodal learning
- scalability dan efisiensi model

""")

    return "\n".join(synthesized)


# =====================================
# BUILD CITATION CONTEXT
# =====================================

def build_citation_context(results: List[Dict]):

    """
    Build thesis-aware citation context
    for grounded academic responses.
    """

    sections = []

    for idx, result in enumerate(
        results,
        start=1
    ):

        payload = result.get(
            "payload",
            {}
        )

        title = payload.get(
            "title",
            "Unknown Title"
        )

        author = payload.get(
            "author",
            "Unknown Author"
        )

        year = payload.get(
            "year",
            "-"
        )

        prodi = payload.get(
            "prodi",
            "-"
        )

        url = payload.get(
            "url",
            "-"
        )

        abstract = payload.get(
            "abstract",
            ""
        )

        chunk = payload.get(
            "chunk",
            ""
        )

        chunk_index = payload.get(
            "chunk_index",
            idx
        )

        score = result.get(
            "rerank_score",
            result.get(
                "score",
                0
            )
        )

        content = chunk.strip()

        if not content:
            content = abstract.strip()

        section = f"""
[SOURCE_{idx}]

SOURCE_ID: {idx}

TITLE:
{title}

AUTHOR:
{author}

YEAR:
{year}

PROGRAM_STUDI:
{prodi}

CHUNK_INDEX:
{chunk_index}

RELEVANCE_SCORE:
{round(score, 4)}

URL:
{url}

CONTENT:
{content}
"""

        sections.append(
            section.strip()
        )

    return "\n\n".join(sections)