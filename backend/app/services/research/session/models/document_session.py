from dataclasses import dataclass, field


# =====================================
# DOCUMENT ITEM
# =====================================

@dataclass
class DocumentItem:

    document_id: str

    filename: str

    file_type: str

    pages: int = 0

    chunks: int = 0

    content: str = ""

    pages_data: list = field(
        default_factory=list
    )


# =====================================
# DOCUMENT SESSION
# =====================================

@dataclass
class DocumentSession:

    documents: dict[
        str,
        DocumentItem
    ] = field(
        default_factory=dict
    )

    # =================================
    # ADD DOCUMENT
    # =================================

    def add_document(
        self,
        document: DocumentItem,
    ):

        self.documents[
            document.document_id
        ] = document

    # =================================
    # GET DOCUMENT
    # =================================

    def get_document(
        self,
        document_id: str,
    ):

        return self.documents.get(
            document_id
        )

    # =================================
    # REMOVE DOCUMENT
    # =================================

    def remove_document(
        self,
        document_id: str,
    ):

        self.documents.pop(
            document_id,
            None,
        )

    # =================================
    # LIST DOCUMENTS
    # =================================

    def list_documents(self):

        return list(
            self.documents.values()
        )

    # =================================
    # TOTAL DOCUMENTS
    # =================================

    def count(self):

        return len(
            self.documents
        )

    # =================================
    # CLEAR
    # =================================

    def clear(self):

        self.documents.clear()

    # =================================
    # SERIALIZER
    # =================================

    def to_dict(self):

        return {

            "documents": [

                document.__dict__

                for document in

                self.documents.values()

            ]

        }
