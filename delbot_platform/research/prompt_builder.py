from __future__ import annotations

from typing import Any


class ResearchPromptBuilder:

    def build(
        self,
        *,
        query: str,
        context: str,
        history: list[dict] | None = None,
        previous: str = "",
        research_state: dict[str, Any] | None = None,
    ) -> list[dict]:

        messages: list[dict] = []

        messages.append(
            {
                "role": "system",
                "content": (
                    "Anda adalah DELBot.\n\n"
                    "Anda adalah AI Research Assistant akademik.\n\n"
                    "Aturan:\n"
                    "1. Gunakan hanya informasi dari dokumen yang diberikan.\n"
                    "2. Jangan membuat sitasi palsu.\n"
                    "3. Jika informasi tidak ditemukan maka katakan tidak ditemukan.\n"
                    "4. Jawaban harus akademik, objektif, dan terstruktur.\n"
                    "5. Gunakan heading bila diperlukan.\n"
                    "6. Pisahkan fakta, analisis, dan kesimpulan.\n"
                    "7. Jangan mengarang informasi di luar konteks dokumen."
                ),
            }
        )

        if research_state:

            topic = research_state.get("topic")
            goal = research_state.get("research_goal")
            summary = research_state.get("summary")
            keywords = research_state.get("keywords", [])
            sources = research_state.get("sources", [])

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "CURRENT RESEARCH STATE\n\n"
                        f"Topic:\n{topic}\n\n"
                        f"Goal:\n{goal}\n\n"
                        f"Summary:\n{summary}\n\n"
                        f"Keywords:\n{keywords}\n\n"
                        f"Known Sources:\n{sources}"
                    ),
                }
            )

        messages.append(
            {
                "role": "system",
                "content": (
                    "DOCUMENT CONTEXT\n\n"
                    f"{context}"
                ),
            }
        )

        if previous:

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "PREVIOUS ANSWER\n\n"
                        f"{previous}"
                    ),
                }
            )

        if history:

            messages.extend(history[-5:])

        messages.append(
            {
                "role": "user",
                "content": query,
            }
        )

        return messages