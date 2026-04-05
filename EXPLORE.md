# Chat conversation here

## Round 1. steph


### Exploring the Problem Space

**Precision that surface immediately:**

### 1. Metric normalization vs flexibility

```
┌─────────────────────────────────────────────────────────┐
│  SOURCE A: {model, score, price_per_token, latency}     │
│  SOURCE B: {model, throughput, context_window, cost}    │
│                                                         │
│  Option A: Store as-is per source (schema-less)         │
│  Option B: Normalize to common fields + source-specific │
│  Option C: Hybrid - common fields + raw extras JSON     │
└─────────────────────────────────────────────────────────┘
```

Option C is the best for the project. Persist each sources. Then have an hybrid model with common fields, and specific fields belonging to each source.

### 2. Re-fetching behavior
When we re-fetch artificialanalysis.ai tomorrow — we do:
- **Insert** new rows with new timestamp (history preserved)

### 3. Source identity
We identify a "source" just with a name (bases on FQDN) and the URL, example: {"artificialanalysis.ai":  "https://artificialanalysis.ai/leaderboards/providers"}

### 4. What's in SOURCES.md exactly
Name and URLs. Does not content other things for this version.
---

**Technical Overview:**
- Database choice SQLite
- Python implementation
- Node will be used for UI afterwards
- Directory structure
  - src/ contains Python file
  - .history/ contains each run of gathering data from sources
    - inside there is a file YYYYMMDD_HHMMSS.log 

---

