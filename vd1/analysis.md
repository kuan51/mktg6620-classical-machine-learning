# Case 1 — Which Customers Should the Retention Team Contact?

Rex Linder · MKTG 6620 · V&D Project 1

## Validation choice (recorded before the final evaluation)

**Date recorded:** 2026-09-28, after running `compare` and before running `evaluate`.

**Chosen method:** `trees` (boosted trees).

Validation table (1,409 validation rows, from `outputs/validation.csv`):

| Method | Validation AUC | Top-20% list size | Churn rate in top-20% list | Overall validation churn rate |
|---|---|---|---|---|
| contract | 0.7427 | 281 | 41.6% | 26.5% |
| logistic | 0.8384 | 281 | 61.2% | 26.5% |
| trees | 0.8456 | 281 | 65.1% | 26.5% |

<!-- TODO(you): 2–3 sentences in your own words explaining why the validation evidence supports this choice. Write them here, then tell Claude to commit and run evaluate. -->

