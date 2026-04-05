"""Read and parse SOURCES.md."""

import re
import logging
from pathlib import Path
from dataclasses import dataclass

log = logging.getLogger(__name__)


@dataclass
class Source:
    name: str
    url: str


def read_sources(sources_path: str | Path = "SOURCES.md") -> list[Source]:
    """Parse SOURCES.md markdown table into list of Source objects.

    Handles malformed entries gracefully by logging a warning and skipping.
    """
    path = Path(sources_path)
    if not path.exists():
        log.warning(f"SOURCES.md not found at {path}")
        return []

    content = path.read_text(encoding="utf-8")
    sources = []

    # Parse markdown table: | name | url | or plain: name url
    for line in content.splitlines():
        line = line.strip()
        cells = []

        if line.startswith("|"):
            # Markdown table format
            cells = [c.strip() for c in line.split("|")[1:-1]]
        elif line and " " in line:
            # Plain space-separated format: name url
            parts = line.split()
            if len(parts) >= 2:
                cells = [parts[0], parts[1]]

        if not cells:
            continue

        name, url = cells[0], cells[1]
        # Skip header-like rows
        if name.lower() in ("name", "source", "url"):
            continue
        if not name or not url:
            log.warning(f"Skipping malformed row: {line}")
            continue
        sources.append(Source(name=name, url=url))

    return sources
