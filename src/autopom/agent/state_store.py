from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from hashlib import sha256
import json


@dataclass(slots=True)
class FrontierItem:
    url: str
    depth: int
    via_action: str = "seed"


@dataclass(slots=True)
class CrawlState:
    frontier: deque[FrontierItem] = field(default_factory=deque)
    visited_signatures: set[str] = field(default_factory=set)
    edge_history: set[tuple[str, str, str]] = field(default_factory=set)
    page_count: int = 0
    duplicate_hits: int = 0

    def enqueue(self, item: FrontierItem) -> None:
        self.frontier.append(item)

    def dequeue(self) -> FrontierItem | None:
        if not self.frontier:
            return None
        return self.frontier.popleft()

    def make_signature(
        self,
        *,
        normalized_url: str,
        dom_fingerprint: str,
        landmarks: list[str],
    ) -> str:
        material = json.dumps(
            {
                "url": normalized_url,
                "dom": dom_fingerprint,
                "landmarks": landmarks,
            },
            sort_keys=True,
        )
        return sha256(material.encode("utf-8")).hexdigest()
