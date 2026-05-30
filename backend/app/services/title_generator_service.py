from app.rag.thesis_retriever import (
    search_thesis_dataset
)

from app.services.llm.model_gateway import (
    gateway
)


def build_context(theses):

    context = ""

    for thesis in theses:

        context += f"""
TITLE:
{thesis.get("title")}

YEAR:
{thesis.get("year")}

ABSTRACT:
{thesis.get("abstract")}

----------------------------------
"""

    return context


def generate_thesis_titles(
    topic: str,
    top_k: int = 10
):

    theses = search_thesis_dataset(
        query=topic,
        top_k=top_k
    )

    context = build_context(theses)

    prompt = f"""
You are a senior thesis advisor.

TOPIC:

{topic}

RELATED THESIS:

{context}

TASKS:

1. Identify research gaps.
2. Identify weaknesses.
3. Identify novelty opportunities.
4. Generate 20 thesis title ideas.

RULES:

- Use only retrieved theses.
- Do not invent unrelated technologies.
- Do not suggest blockchain unless retrieved.
- Do not suggest IoT unless retrieved.
- Do not suggest AI unless retrieved.
- Focus on realistic undergraduate thesis topics.

FORMAT:

# Research Gaps

# Weaknesses

# Novelty Opportunities

# Thesis Title Ideas
"""

    response = gateway.generate_response(
        prompt=prompt
    )

    return {
        "topic": topic,
        "related_theses": theses,
        "result": response
    }