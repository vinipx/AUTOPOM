from __future__ import annotations


INTERACTIVE_TAGS = {"a", "button", "input", "select", "textarea"}


def compact_dom(raw_nodes: list[dict], max_nodes: int = 120) -> dict:
    """
    Reduce raw node capture to interactive, high-signal context only.
    Expected node shape keys: tag, role, text, attributes, selector, section
    """
    kept: list[dict] = []
    for node in raw_nodes:
        tag = str(node.get("tag", "")).lower()
        role = str(node.get("role", "")).lower()
        is_interactive = (
            tag in INTERACTIVE_TAGS
            or role in {"button", "textbox", "link", "combobox", "checkbox"}
            or "tabindex" in node.get("attributes", {})
        )
        if not is_interactive:
            continue
        kept.append(
            {
                "role": role or "generic",
                "label": node.get("text") or node.get("ariaLabel") or "Element",
                "selector": node.get("selector", ""),
                "section": node.get("section", "mainContent"),
            }
        )
        if len(kept) >= max_nodes:
            break

    landmarks = sorted({str(node.get("section", "mainContent")) for node in kept})
    fingerprint = f"compact::{len(kept)}::{','.join(landmarks)}"
    links = [node["selector"] for node in kept if node.get("role") == "link"]
    return {
        "fingerprint": fingerprint,
        "landmarks": landmarks,
        "elements": kept,
        "links": links,
    }
