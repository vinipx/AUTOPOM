from __future__ import annotations


def infer_icon_semantic_name(visible_hint: str) -> str | None:
    """
    Small heuristic mapper used before expensive vision model calls.
    """
    normalized = visible_hint.strip().lower()
    if normalized in {"x", "close", "dismiss"}:
        return "closeModalButton"
    if normalized in {"☰", "menu", "hamburger"}:
        return "openMenuButton"
    if normalized in {"🔍", "search"}:
        return "searchButton"
    return None
