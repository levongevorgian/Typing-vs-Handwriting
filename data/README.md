# Data dictionary and provenance

`laptop_urry.csv` is copied unchanged from the project's earlier Stage 1. Its source was the public CSV endpoint for `afex::laptop_urry`: https://singmann.r-universe.dev/afex/data/laptop_urry/csv . The source describes Urry et al.'s (2021) replication data. The input fingerprint is saved in `results/data_audit.json`.

| Column | Meaning |
|---|---|
| pid | Pseudonymous participant identifier; 142 unique values |
| condition | `laptop` = typing (68); `longhand` = handwriting (74) |
| talk | Recorded lecture: algorithms, ideas, indus, inequalities or islam |
| overall | Packaged overall memory score, 0–100 |
| factual | Factual-question score, 0–100 |
| conceptual | Conceptual-question score, 0–100 |

One row represents one participant. Factual and conceptual scores in the same row are paired. The packaged overall score is used as supplied; it is not reconstructed by assuming equal weighting of factual and conceptual scores. No rows are removed or imputed. An IQR flag is descriptive and does not trigger deletion.

Derived fields in memory: `typing` (1 for laptop, otherwise 0), `gap` (conceptual minus factual). Lecture indicators use algorithms as reference. An illustrative category uses overall >= 70; this is not an official pass/fail definition. Scores are percentage points, not raw numbers of correctly answered questions.

Identifiers are research codes from the public package, not names. The dataset lacks demographics, note length, verbatim overlap, sessions, timestamps, individual quiz items and delayed follow-up.
