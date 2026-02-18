from __future__ import annotations

import json
from pathlib import Path

from autopom.extraction.schema import PageModel


class Persistence:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.models_dir = output_dir / "models_json"
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def write_page_model(self, page: PageModel) -> Path:
        target = self.models_dir / f"{page.page_name}.json"
        with target.open("w", encoding="utf-8") as f:
            json.dump(page.to_dict(), f, indent=2)
        return target
