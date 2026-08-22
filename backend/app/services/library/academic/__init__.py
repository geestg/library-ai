from __future__ import annotations

from app.services.library.academic.intent_router import route_intent, contains_keyword
from app.services.library.academic.book_formatter import normalize_book, deduplicate_books, build_sources
from app.services.library.academic.intent_handlers import AcademicIntentHandlers
