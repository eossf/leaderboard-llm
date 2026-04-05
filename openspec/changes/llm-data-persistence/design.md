## Context

We need a simple, script-driven data pipeline that fetches LLM leaderboard data from web sources, parses it, and persists it to a local SQLite database. Sources are managed in a `SOURCES.md` file. The system must handle multiple source types with different data schemas, and never lose historical data.

Current state: Greenfield project. No existing code.

## Goals / Non-Goals

**Goals:**
- Fetch data from sources defined in `SOURCES.md` via HTTP
- Convert HTML responses to structured JSON using per-source adapters
- Persist raw blobs and parsed rows to SQLite
- Support running single source (`--source=<name>`) or all sources (`--all`)
- Handle errors gracefully — one source failure does not block others

**Non-Goals:**
- No UI, API, or backend service
- No cross-source ranking queries
- No scheduling or daemon mode
- No automatic source discovery
- No re-parsing of old raw blobs in v0.0.1

## Decisions

### 1. SQLite as the persistence layer

**Decision:** Use `data/leaderboard.sqlite` with two tables — `Source` for raw blobs and `Source_mapping` for parsed rows.

**Rationale:** SQLite is zero-config, file-based, and ships with Python stdlib. The hybrid data model (fixed columns + JSON extras) handles schema variation without schema-less complexity. The `.sqlite` file is portable and can be committed to git.

**Alternatives considered:**
- MongoDB: Excellent schema flexibility but requires a running server, overkill for a local script
- PostgreSQL: Heavy for a local-first app, adds deployment complexity

---

### 2. Hybrid data model: fixed columns + JSON extras

**Decision:** `Source_mapping` has fixed columns (`id`, `source_id`, `model_name`) plus an `extras TEXT` JSON column for source-specific fields.

**Rationale:** Common fields (`model_name`) are queryable as SQL columns. Source-specific variance goes into `extras` JSON, avoiding column proliferation when new sources have different fields.

---

### 3. Per-source adapter pattern

**Decision:** Each source has its own adapter module under `src/adapters/` with two responsibilities: `fetch()` (HTML retrieval) and `parse()` (HTML → JSON → structured dict).

**Rationale:** Sources return different HTML structures. Isolating each source's fetching and parsing into its own adapter keeps the core pipeline simple and makes adding new sources a matter of dropping in a new adapter file.

**Adapter interface:**
```python
def fetch(url: str) -> str:          # returns raw HTML string
def parse(html: str, schema_ver: int) -> list[dict]:  # returns list of model rows
```

---

### 4. SOURCES.md as a markdown table

**Decision:** `SOURCES.md` is a markdown table with columns `name` and `url`.

**Rationale:** Human-editable, git-friendly, zero parsing complexity for v0.0.1. No YAML or JSON config files to maintain.

---

### 5. GRACEFUL SKIP error handling

**Decision:** If a source fails (network error, parse error, etc.), log a warning and continue to the next source. Persist whatever succeeded.

**Rationale:** We never want one bad source to block the entire pipeline. Persisting partial results is more valuable than failing the entire run.

---

### 6. Schema version tracking per adapter

**Decision:** Each adapter has a `SCHEMA_VERSION = 1` constant. When source structure changes, increment the version. The `schema_version` is stored in `Source_mapping` rows.

**Rationale:** Enables future re-parsing of old raw blobs with the correct adapter version. Decouples historical data from current parser logic.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Source changes HTML structure without notice | Adapters encapsulate parsing logic; update adapter + bump schema_version |
| SOURCES.md has malformed entries | Log warning and skip entry; do not crash |
| SQLite schema changes needed mid-project | ALTER TABLE is possible; JSON extras absorbs most variance without migrations |
| New source has radically different shape | Write new adapter; no core code changes needed |

## Migration Plan

v0.0.1 is a greenfield project — no existing data to migrate.

1. Create `src/` directory structure
2. Implement `run.py` CLI
3. Implement `artificialanalysis.ai` adapter as the first source
4. Run `python run.py --source=artificialanalysis.ai`
5. Verify `data/leaderboard.sqlite` has correct tables and data
6. Commit to git

## Open Questions

- Should we use `pip` or `micromamba` for dependency management? (Currently micromamba for environment)
- What is the exact HTML structure of artificialanalysis.ai? We need to inspect and write the first adapter.
- Should `data/` directory be git-ignored or committed? (Trade-off: DB file is large but persists history)
