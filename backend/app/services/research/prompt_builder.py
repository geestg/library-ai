# =====================================
# BUILD STRUCTURED EVIDENCE
# =====================================

def build_evidence_section(
    evidence: dict
):

    technologies = evidence.get(
        "technologies",
        []
    )

    methodologies = evidence.get(
        "methodologies",
        []
    )

    keywords = evidence.get(
        "keywords",
        []
    )

    research_domains = evidence.get(
        "research_domains",
        []
    )

    lines = []

    lines.append(
        "STRUCTURED EVIDENCE"
    )

    lines.append(
        "=" * 50
    )

    # =================================
    # TECHNOLOGIES
    # =================================

    lines.append(
        "\nTECHNOLOGIES:"
    )

    if technologies:

        for item in technologies:

            lines.append(
                f"- {item['name']} ({item['count']})"
            )

    else:

        lines.append(
            "- Not found"
        )

    # =================================
    # METHODOLOGIES
    # =================================

    lines.append(
        "\nMETHODOLOGIES:"
    )

    if methodologies:

        for item in methodologies:

            lines.append(
                f"- {item['name']} ({item['count']})"
            )

    else:

        lines.append(
            "- Not found"
        )

    # =================================
    # KEYWORDS
    # =================================

    lines.append(
        "\nKEYWORDS:"
    )

    if keywords:

        for item in keywords[:20]:

            lines.append(
                f"- {item['name']} ({item['count']})"
            )

    else:

        lines.append(
            "- Not found"
        )

    # =================================
    # RESEARCH DOMAINS
    # =================================

    lines.append(
        "\nRESEARCH DOMAINS:"
    )

    if research_domains:

        for item in research_domains:

            lines.append(
                f"- {item['name']} ({item['count']})"
            )

    else:

        lines.append(
            "- Not found"
        )

    return "\n".join(
        lines
    )


# =====================================
# BUILD EVIDENCE MATRIX
# =====================================

def build_matrix_section(
    matrix: dict
):

    lines = []

    lines.append(
        "EVIDENCE MATRIX"
    )

    lines.append(
        "=" * 50
    )

    # =================================
    # TECHNOLOGY FREQUENCY
    # =================================

    lines.append(
        "\nTECHNOLOGY FREQUENCY:"
    )

    technology_frequency = matrix.get(
        "technology_frequency",
        {}
    )

    if technology_frequency:

        for name, count in technology_frequency.items():

            lines.append(
                f"- {name} ({count})"
            )

    else:

        lines.append(
            "- Not found"
        )

    # =================================
    # METHODOLOGY FREQUENCY
    # =================================

    lines.append(
        "\nMETHODOLOGY FREQUENCY:"
    )

    methodology_frequency = matrix.get(
        "methodology_frequency",
        {}
    )

    if methodology_frequency:

        for name, count in methodology_frequency.items():

            lines.append(
                f"- {name} ({count})"
            )

    else:

        lines.append(
            "- Not found"
        )

    # =================================
    # DOMAIN FREQUENCY
    # =================================

    lines.append(
        "\nDOMAIN FREQUENCY:"
    )

    domain_frequency = matrix.get(
        "domain_frequency",
        {}
    )

    if domain_frequency:

        for name, count in domain_frequency.items():

            lines.append(
                f"- {name} ({count})"
            )

    else:

        lines.append(
            "- Not found"
        )

    return "\n".join(
        lines
    )


# =====================================
# RESEARCH ANALYSIS PROMPT
# =====================================

def build_research_prompt(

    query: str,

    evidence_text: str,

    citation_context: str,

    mode: str = "analysis"
):

    return f"""
You are DELBot.

AI Academic Knowledge Operating System.

==================================================
RESEARCH TOPIC
==================================================

{query}

==================================================
STRUCTURED EVIDENCE
==================================================

{evidence_text}

==================================================
RETRIEVED SOURCES
==================================================

{citation_context}

==================================================
STRICT GROUNDING RULES
==================================================

1. Use ONLY retrieved sources.

2. Use ONLY technologies found
inside STRUCTURED EVIDENCE.

3. Use ONLY methodologies found
inside STRUCTURED EVIDENCE.

4. Never invent:
- AI models
- frameworks
- architectures
- technologies
- datasets
- methodologies

5. If information is not found:

"Insufficient evidence from retrieved theses."

6. Every factual claim
must contain citation.

7. Citation format:

[1]
[2]
[3]

Never use:

(Source_1)
(Source_2)

==================================================
IMPORTANT STATISTICAL RULES
==================================================

Technology or methodology
with frequency = 1

MUST NOT be described as:

- dominant
- common
- widely used
- major trend

Technology or methodology
with frequency >= 2

may be described as trend.

Technology or methodology
with frequency >= 3

may be described as dominant.

==================================================
TASKS
==================================================

1. Executive Summary
2. Research Themes
3. Technologies
4. Methodologies
5. Weaknesses
6. Research Gaps
7. Novelty Opportunities
8. Future Directions
9. Thesis Titles
10. Recommendation

==================================================
OUTPUT FORMAT
==================================================

# Executive Summary

# Common Research Themes

# Technologies Used

# Methodologies Used

# Weaknesses of Existing Studies

# Research Gaps

# Novelty Opportunities

# Future Research Directions

# Recommended Thesis Titles

# Final Recommendation
"""