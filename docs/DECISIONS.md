# Decisions (append-only)

Never edit a past entry. Reverse one by adding a new entry that says "Supersedes DEC-0NN".

## DEC-001 — Carry boosted trees forward to the final test (2026-09-28)

Chosen: `trees`, the highest validation AUC (0.8456 vs logistic 0.8384 vs contract 0.7427), per the handout default.
Rejected: `logistic` (0.007 lower AUC, simpler and more explainable; a defensible alternative), `contract` (clearly lower ranking and list churn rate on validation).
Accepted gaps: the AUC gap to logistic is small and may not survive the final test; trees are harder to explain to a business reader.
Recorded before `evaluate` was run; the student's own reasoning is in `vd1/analysis.md`.
