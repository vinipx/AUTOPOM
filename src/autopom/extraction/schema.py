from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(slots=True)
class SourceEvidence:
    dom: bool = True
    vision: bool = False


@dataclass(slots=True)
class ElementModel:
    element_id: str
    type: str
    role: str
    semantic_label: str
    selector: str
    fallback_selectors: list[str] = field(default_factory=list)
    confidence: float = 0.8
    section: str = "mainContent"
    source: SourceEvidence = field(default_factory=SourceEvidence)


@dataclass(slots=True)
class ActionModel:
    name: str
    params: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    post_condition: str | None = None


@dataclass(slots=True)
class SectionModel:
    name: str
    elements: list[ElementModel] = field(default_factory=list)


@dataclass(slots=True)
class PageModel:
    page_id: str
    page_name: str
    url: str
    route: str
    requires_auth: bool = False
    sections: list[SectionModel] = field(default_factory=list)
    actions: list[ActionModel] = field(default_factory=list)
    discovered_links: list[str] = field(default_factory=list)
    next_navigation_hints: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
