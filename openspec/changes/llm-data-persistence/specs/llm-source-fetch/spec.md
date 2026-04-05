## ADDED Requirements

### Requirement: Source registry is readable at runtime
The system SHALL read `SOURCES.md` at runtime to discover available sources. Each entry contains a source name and URL.

#### Scenario: SOURCES.md parsed correctly
- **WHEN** `run.py` starts
- **THEN** it SHALL parse `SOURCES.md` as a markdown table with columns `name` and `url`
- **AND** it SHALL build a list of `{name, url}` pairs

#### Scenario: SOURCES.md contains multiple sources
- **WHEN** `SOURCES.md` contains entries for `source-a` and `source-b`
- **THEN** `run.py --all` SHALL attempt to fetch both sources in sequence

---

### Requirement: Source is fetched and persisted
For each source, the system SHALL fetch the HTML content from the source URL and persist it to the SQLite database.

#### Scenario: Successful fetch and persist
- **WHEN** `run.py --source=artificialanalysis.ai` is invoked
- **THEN** the system SHALL fetch `https://artificialanalysis.ai/leaderboards/providers`
- **AND** SHALL store a raw blob in `Source.raw` with `fetched_at` set to current timestamp
- **AND** SHALL parse the response into structured model data
- **AND** SHALL store rows in `Source_mapping` table

#### Scenario: Fetch fails with network error
- **WHEN** source URL returns a non-200 HTTP status or network timeout
- **THEN** the system SHALL log a warning for that source
- **AND** SHALL continue to next source (GRACEFUL SKIP)

---

### Requirement: Raw blob is immutable after insert
The `Source.raw` field SHALL NOT be modified or deleted after insertion. Each run creates a new `Source` row.

#### Scenario: Re-running the same source creates new row
- **WHEN** `run.py --source=artificialanalysis.ai` runs on day 1 and again on day 2
- **THEN** two `Source` rows SHALL exist — one per run
- **AND** no existing row SHALL be modified

---

### Requirement: Parsed rows include source-specific extras
Each `Source_mapping` row SHALL contain a `model_name` (common field) and an `extras` JSON field for source-specific fields.

#### Scenario: Model data stored with extras
- **WHEN** source returns model data with fields `{name, score, latency, price}`
- **THEN** the system SHALL store `model_name` in `Source_mapping.model_name`
- **AND** SHALL store the full source-specific payload as JSON in `extras`

---

### Requirement: CLI supports single source and all-sources modes
The CLI SHALL support `--source=<name>` to fetch a single named source, and `--all` to iterate all sources in `SOURCES.md`.

#### Scenario: Single source mode
- **WHEN** `python run.py --source=artificialanalysis.ai` is invoked
- **THEN** the system SHALL fetch only the `artificialanalysis.ai` source
- **AND** SHALL ignore all other entries in `SOURCES.md`

#### Scenario: All sources mode
- **WHEN** `python run.py --all` is invoked
- **THEN** the system SHALL iterate all sources in `SOURCES.md`
- **AND** SHALL fetch and persist each in sequence
