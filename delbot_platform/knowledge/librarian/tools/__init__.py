from delbot_platform.knowledge.librarian.tools.circulation import LibraryCirculationTools
from delbot_platform.knowledge.librarian.tools.dataset_tool import LibraryDatasetTools
from delbot_platform.knowledge.librarian.tools.visitor import LibraryVisitorTools

class LibraryLibrarianTools(LibraryCirculationTools, LibraryDatasetTools, LibraryVisitorTools):
    """
    Facade class yang menggabungkan seluruh perkakas (tools) Pustakawan Perpustakaan
    untuk menyederhanakan pemanggilan di sisi agen.
    """
    pass
