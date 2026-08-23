from __future__ import annotations

from typing import Dict, List, Tuple, Any, Optional

DOMINANT_THRESHOLD = 3
RECENT_YEAR_THRESHOLD = 1
LONG_SPAN_THRESHOLD = 5

def normalize_frequency(frequency) -> dict:
    if frequency is None:
        return {}
    if isinstance(frequency, dict):
        return frequency
    return dict(frequency)

def unique_keep_order(items) -> list:
    seen = set()
    results = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        results.append(item)
    return results

def get_dominant_items(frequency, threshold: int = DOMINANT_THRESHOLD) -> list:
    frequency = normalize_frequency(frequency)
    return [name for name, count in frequency.items() if count >= threshold]

def get_emerging_items(frequency) -> list:
    frequency = normalize_frequency(frequency)
    return [name for name, count in frequency.items() if count == 2]

def get_rare_items(frequency) -> list:
    frequency = normalize_frequency(frequency)
    return [name for name, count in frequency.items() if count == 1]

def get_top_item(frequency) -> Optional[Tuple[str, int]]:
    frequency = normalize_frequency(frequency)
    if not frequency:
        return None
    return max(frequency.items(), key=lambda item: item[1])

def get_sorted_items(frequency) -> list:
    frequency = normalize_frequency(frequency)
    return sorted(frequency.items(), key=lambda item: item[1], reverse=True)
