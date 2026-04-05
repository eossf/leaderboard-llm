## 1. Project Structure Setup

- [ ] 1.1 Create `src/` directory with `__init__.py`
- [ ] 1.2 Create `src/adapters/` directory with `__init__.py`
- [ ] 1.3 Create `data/` directory (gitignored for now)
- [ ] 1.4 Add dependencies: `requests`, `beautifulsoup4` to environment

## 2. SQLite Database Schema

- [ ] 2.1 Create `src/db.py` with `init_db()` function
- [ ] 2.2 Define `Source` table: `id` (INTEGER PK), `fetched_at`, `source_name`, `url`, `raw`
- [ ] 2.3 Define `Source_mapping` table: `id` (INTEGER PK), `source_id` (FK), `model_name`, `extras` (TEXT JSON), `schema_version`
- [ ] 2.4 Verify schema with SQLite CLI

## 3. SOURCES.md Reader

- [ ] 3.1 Create `src/sources.py` with `read_sources()` function
- [ ] 3.2 Parse markdown table with `name | url` columns
- [ ] 3.3 Handle malformed entries gracefully (log + skip)

## 4. Source Adapter: artificialanalysis.ai

- [ ] 4.1 Inspect HTML structure of `https://artificialanalysis.ai/leaderboards/providers`
- [ ] 4.2 Create `src/adapters/artificialanalysis.py`
- [ ] 4.3 Implement `fetch(url)` → returns raw HTML string
- [ ] 4.4 Implement `parse(html)` → returns list of model dicts with `model_name` and source-specific fields
- [ ] 4.5 Set `SCHEMA_VERSION = 1` constant

## 5. Core Pipeline (`run.py`)

- [ ] 5.1 Create `run.py` CLI entry point
- [ ] 5.2 Implement `--source=<name>` argument parsing
- [ ] 5.3 Implement `--all` argument (default)
- [ ] 5.4 Wire: read SOURCES.md → for each source → fetch → parse → persist
- [ ] 5.5 Implement GRACEFUL SKIP error handling

## 6. Persistence Layer

- [ ] 6.1 Insert raw blob into `Source` table
- [ ] 6.2 Insert parsed rows into `Source_mapping` table
- [ ] 6.3 Verify immutability: no UPDATE/DELETE on existing rows

## 7. First Integration Run

- [ ] 7.1 Run `python run.py --source=artificialanalysis.ai`
- [ ] 7.2 Verify `data/leaderboard.sqlite` has data
- [ ] 7.3 Run `python run.py --all` and verify all sources processed
- [ ] 7.4 Re-run and verify history preserved (new rows, not updates)
