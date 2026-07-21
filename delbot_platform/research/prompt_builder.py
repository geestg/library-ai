from __future__ import annotations



class ResearchPromptBuilder:



    def build(

        self,

        query:str,

        context:str

    ):


        return f"""

Anda adalah DELBot, sistem AI Research Assistant.

Jawab pertanyaan penelitian berdasarkan sumber berikut.

PERTANYAAN:

{query}


SUMBER AKADEMIK:

{context}


Instruksi:

1. Gunakan hanya informasi dari sumber.
2. Jangan membuat referensi palsu.
3. Berikan penjelasan akademik.
4. Sertakan sumber halaman jika tersedia.

Jawaban:

"""
