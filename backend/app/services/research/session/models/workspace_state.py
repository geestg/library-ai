from dataclasses import dataclass
from dataclasses import field

from typing import Any


# =====================================
# WORKSPACE STATE
# =====================================

@dataclass
class WorkspaceState:

    selected_citation: Any = None

    selected_thesis: Any = None

    last_search: str = ""

    filters: dict = field(
        default_factory=dict
    )

    ui_state: dict = field(
        default_factory=dict
    )

    # =====================================
    # CLEAR
    # =====================================

    def clear(self):

        self.selected_citation = None

        self.selected_thesis = None

        self.last_search = ""

        self.filters.clear()

        self.ui_state.clear()

    # =====================================
    # SERIALIZE
    # =====================================

    def to_dict(self):

        return {

            "selected_citation":
                self.selected_citation,

            "selected_thesis":
                self.selected_thesis,

            "last_search":
                self.last_search,

            "filters":
                self.filters,

            "ui_state":
                self.ui_state,

        }

