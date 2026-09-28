# Conventions (current state)

- One folder per course project: `vd1/` holds V&D Project 1 (Case 1). Later projects get `vd2/`, etc.
- Python 3.11 in `.venv/` at the repo root, packages pinned by `vd1/VD1_requirements.txt`
  (numpy 1.24.2, pandas 2.0.0, scikit-learn 1.2.2). `.venv/` is not committed.
- `vd1/churn.csv` is the course-supplied data and is not committed; obtain it from Canvas.
- The supplied `VD1_analysis.py` is used unchanged. Run from inside `vd1/`:
  `../.venv/bin/python VD1_analysis.py compare --csv churn.csv --out outputs`
  `../.venv/bin/python VD1_analysis.py evaluate --csv churn.csv --out outputs --choice <method>`
- `vd1/outputs/` is committed (the grader reads it). Console output is saved next to it as `*_stdout.txt`.
- Assessed prose (interpretations, Q4 reasons, memo) is written by the student; AI runs, explains,
  and fills tables. AI help is recorded in `vd1/ai_use/`.
- Commits: Conventional Commits, one kind of change per commit, never on `master` directly.
- `docs/DECISIONS.md` is append-only; `docs/RUNLOG.md` logs intent, then verified results, with the exact command.
