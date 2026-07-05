from dataclasses import dataclass, field


@dataclass
class WorkspaceState:

    selected_citation = None

    selected_thesis = None

    last_search: str = ""

    filters: dict = field(
        default_factory=dict
    )

    ui_state: dict = field(
        default_factory=dict
    )

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