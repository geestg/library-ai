from app.services.librarian.tools.circulation import LibraryCirculationTools
from app.services.librarian.tools.dataset_tool import LibraryDatasetTools
from app.services.librarian.tools.visitor import LibraryVisitorTools

class LibraryLibrarianTools(LibraryCirculationTools, LibraryDatasetTools, LibraryVisitorTools):
    """
    Facade class yang menggabungkan seluruh perkakas (tools) Pustakawan Perpustakaan
    untuk menyederhanakan pemanggilan di sisi agen.
    """
    pass
