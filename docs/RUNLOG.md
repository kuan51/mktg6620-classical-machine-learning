# Run log

Format: date, PLAN (what will be done) or DONE (what was verified, with the exact command), or SKIPPED.

## 2026-09-28

- DONE: created `.venv` and installed pins. Check: `.venv/bin/python -c "import numpy,pandas,sklearn;print(numpy.__version__,pandas.__version__,sklearn.__version__)"` printed `1.24.2 2.0.0 1.2.2`.
- DONE: extracted the assignment zip into `vd1/`. `sha256sum vd1/churn.csv` = `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`.
- PLAN: run the compare stage from `vd1/`: `../.venv/bin/python VD1_analysis.py compare --csv churn.csv --out outputs`.
