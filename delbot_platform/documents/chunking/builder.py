from __future__ import annotations

import uuid


from delbot_platform.documents.chunking.chunk import (
    DocumentChunk,
)

from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)

from delbot_platform.documents.structure.section_node import (
    SectionNode,
)


class ChunkBuilder:


    def __init__(
        self,
        max_characters: int = 1200,
    ) -> None:

        self.max_characters = max_characters



    def build(
        self,
        nodes: list[SectionNode],
        document_id: str,
        source: str,
    ) -> list[DocumentChunk]:


        chunks: list[DocumentChunk] = []


        for node in nodes:

            self._process_node(
                node,
                chunks,
                document_id,
                source,
            )


        return chunks



    def _process_node(
        self,
        node: SectionNode,
        chunks: list[DocumentChunk],
        document_id: str,
        source: str,
    ):


        content = self._collect_content(
            node,
        )


        if (
            content.strip()
            and node.title.lower()
            != "document"
        ):


            pages = self._pages(
                node,
            )


            parts = self._split(
                content,
            )


            for index, part in enumerate(parts):


                metadata = ChunkMetadata(

                    document_id=document_id,

                    source=source,

                    section=node.title,

                    level=node.level,

                    page_start=(
                        pages[0]
                        if pages
                        else None
                    ),

                    page_end=(
                        pages[-1]
                        if pages
                        else None
                    ),

                    chapter=self._chapter(
                        node.title,
                    ),

                    chunk_index=index,
                )


                chunks.append(

                    DocumentChunk(

                        id=str(
                            uuid.uuid4()
                        ),

                        content=part,

                        metadata=metadata,
                    )

                )


        for child in node.children:

            self._process_node(
                child,
                chunks,
                document_id,
                source,
            )



    def _collect_content(
        self,
        node: SectionNode,
    ) -> str:


        texts = []


        for block in node.blocks:

            text = block.text.strip()


            if text:

                texts.append(
                    text
                )


        return "\n".join(
            texts
        )



    def _pages(
        self,
        node: SectionNode,
    ) -> list[int]:


        pages = []


        for block in node.blocks:

            pages.append(
                block.page
            )


        return sorted(
            set(pages)
        )



    def _chapter(
        self,
        title: str,
    ) -> str | None:


        if title.upper().startswith(
            "BAB"
        ):

            return title


        return None



    def _split(
        self,
        text: str,
    ) -> list[str]:


        if len(text) <= self.max_characters:

            return [
                text
            ]


        result = []

        current = ""


        for sentence in text.split("."):


            sentence = sentence.strip()


            if not sentence:

                continue


            if (
                len(current)
                + len(sentence)
                >
                self.max_characters
            ):

                result.append(
                    current.strip()
                )

                current = sentence


            else:

                current += (
                    sentence
                    + ". "
                )


        if current.strip():

            result.append(
                current.strip()
            )


        return result