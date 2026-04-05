## Why

LLM leaderboard data is scattered across multiple web sources. Manually tracking and comparing models across sources is error-prone and time-consuming. We need a simple, repeatable way to fetch data from any new source and persist it locally for historical analysis — without losing previously collected data.

## What Changes

- New `SOURCES.md` file listing source names and URLs
- New Python CLI (`run.py`) that reads `SOURCES.md`, fetches each source, and persists to SQLite
- New SQLite database (`data.leaderboard.sqlite`) with two tables: `Source` (raw blobs) and `Source_mapping` (parsed rows with JSON extras)
- Per-source adapter pattern for fetching and parsing HTML sources
- GRACEFUL SKIP error handling — one failed source does not block others
- Schema registration for new source types

## Capabilities

### New Capabilities
- `llm-source-fetch`: Fetch and persist LLM leaderboard data from web sources. Reads sources from `SOURCES.md`, fetches HTML, converts to structured data via per-source adapters, and persists raw blob + parsed rows to SQLite.
- `llm-source-schema`: Schema registration for each source. Tracks parser version and extracted field structure so future re-parsing of raw blobs is possible.

### Modified Capabilities
<!-- No existing specs — this is a greenfield project -->

## Impact

- New file: `SOURCES.md` — curated source registry
- New directory: `src/` — Python application code
- New file: `data/leaderboard.db` (SQLite database)
- New CLI entry point: `python run.py --all` / `python run.py --source=<name>`
- Dependencies: Python 3.13+, `requests`, `beautifulsoup4` (for HTML parsing), Python stdlib `sqlite3`
