## ADDED Requirements

### Requirement: Schema version is tracked per source run
Each `Source_mapping` row SHALL contain a `schema_version` field indicating which parser produced the row.

#### Scenario: Schema version recorded
- **WHEN** a source is parsed by adapter version 1
- **THEN** the system SHALL store `schema_version = 1` in the resulting `Source_mapping` rows

---

### Requirement: New source requires schema registration
When a new source is added to `SOURCES.md`, the system SHALL register its schema before first fetch.

#### Scenario: New source schema registered
- **WHEN** a new source `newsource.ai` is added to `SOURCES.md` and first fetched
- **THEN** the adapter for `newsource.ai` SHALL be registered with a schema version
- **AND** the adapter SHALL extract the known field structure from the raw response

---

### Requirement: Existing source schema can be updated
When a source changes its output structure, the system SHALL allow schema version increment without losing historical data.

#### Scenario: Schema updated for new source version
- **WHEN** source `source-a` changes its output field names
- **THEN** a new adapter version SHALL be registered with incremented `schema_version`
- **AND** new runs SHALL use the updated adapter
- **AND** old raw blobs SHALL remain accessible for re-parsing with old adapters
