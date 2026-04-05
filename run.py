#!/usr/bin/env python3
"""LLM Leaderboard Data Fetcher — CLI entry point.

Usage:
    python run.py --all                 Fetch all sources in SOURCES.md
    python run.py --source=<name>       Fetch a single source by name
"""

import argparse
import logging
import sys
from pathlib import Path

from src.db import init_db, insert_source, insert_model_row
from src.sources import read_sources
from src import adapters

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
log = logging.getLogger(__name__)

from src.adapters import artificialanalysis

ADAPTERS = {
    "artificialanalysis.ai": artificialanalysis,
}


def run_source(source_name: str, url: str) -> bool:
    """Fetch a single source, parse, and persist. Returns True on success."""
    adapter = ADAPTERS.get(source_name)
    if not adapter:
        log.error(f"No adapter found for source: {source_name}")
        return False

    try:
        raw_html = adapter.fetch(url)
    except Exception as e:
        log.warning(f"Failed to fetch {source_name}: {e}")
        return False

    try:
        model_rows = adapter.parse(raw_html)
    except Exception as e:
        log.warning(f"Failed to parse {source_name}: {e}")
        return False

    source_id = insert_source(source_name, url, raw_html)

    for row in model_rows:
        insert_model_row(
            source_id=source_id,
            model_name=row["model_name"],
            extras=row["extras"],
            schema_version=row.get("schema_version", adapter.SCHEMA_VERSION),
        )

    log.info(f"Persisted {len(model_rows)} rows for {source_name}")
    return True


def run_all() -> None:
    """Run all sources defined in SOURCES.md with GRACEFUL SKIP."""
    sources = read_sources()
    if not sources:
        log.error("No sources found in SOURCES.md")
        return

    log.info(f"Found {len(sources)} sources in SOURCES.md")
    for src in sources:
        log.info(f"Processing source: {src.name}")
        success = run_source(src.name, src.url)
        if success:
            log.info(f"✓ {src.name} completed")
        else:
            log.warning(f"✗ {src.name} failed — continuing to next source")


def run_single(source_name: str) -> None:
    """Run a single named source."""
    sources = read_sources()
    matched = [s for s in sources if s.name == source_name]
    if not matched:
        log.error(f"Source not found: {source_name}")
        sys.exit(1)

    src = matched[0]
    success = run_source(src.name, src.url)
    if success:
        log.info(f"✓ {src.name} completed")
        sys.exit(0)
    else:
        log.error(f"✗ {src.name} failed")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM Leaderboard Data Fetcher")
    parser.add_argument(
        "--source",
        metavar="<name>",
        help="Fetch a single source by name from SOURCES.md",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Fetch all sources defined in SOURCES.md (default)",
    )
    args = parser.parse_args()

    init_db()

    if args.source:
        run_single(args.source)
    else:
        run_all()


if __name__ == "__main__":
    main()
