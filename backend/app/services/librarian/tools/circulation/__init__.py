from __future__ import annotations

from app.services.librarian.tools.circulation.circulation_manager import CirculationManagerTool


class LibraryCirculationTools(CirculationManagerTool):
    """
    Facade class yang menggabungkan seluruh perkakas (tools) Sirkulasi & Denda Buku
    untuk menyederhanakan pemanggilan di sisi agen pustakawan.
    """
    pass
