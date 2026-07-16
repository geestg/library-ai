from __future__ import annotations

import re

from delbot_platform.documents.structure.section_node import (
    SectionNode,
)


class SectionHierarchyBuilder:


    def build(
        self,
        sections,
    ) -> list[SectionNode]:


        roots: list[SectionNode] = []

        stack: list[SectionNode] = []


        for section in sections:


            level = self._detect_level(
                section.title,
            )


            node = SectionNode(
                title=section.title,
                level=level,
                blocks=section.blocks,
            )


            while (
                stack
                and stack[-1].level >= level
            ):

                stack.pop()



            if stack:

                stack[-1].children.append(
                    node,
                )

            else:

                roots.append(
                    node,
                )


            stack.append(
                node,
            )


        return roots



    def _detect_level(
        self,
        title: str,
    ) -> int:


        text = title.strip().upper()


        if re.match(
            r"^BAB\s+[IVXLCDM]+",
            text,
        ):

            return 1


        if re.match(
            r"^\d+\.\d+\.\d+",
            title,
        ):

            return 3


        if re.match(
            r"^\d+\.\d+",
            title,
        ):

            return 2


        return 4