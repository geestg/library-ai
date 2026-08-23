from __future__ import annotations

from delbot_platform.knowledge.librarian.tools.visitor.visitor_analytics import VisitorAnalyticsTool
from delbot_platform.knowledge.librarian.tools.visitor.visitor_search import VisitorSearchTool


class LibraryVisitorTools(VisitorAnalyticsTool, VisitorSearchTool):
    """
    Facade class yang menggabungkan seluruh perkakas (tools) Analisis & Pencarian Pengunjung
    untuk menyederhanakan pemanggilan di sisi agen pustakawan.
    """
    pass
