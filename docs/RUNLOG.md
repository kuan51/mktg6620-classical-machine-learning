# Run log

Format: date, PLAN (what will be done) or DONE (what was verified, with the exact command), or SKIPPED.

## 2026-09-28

- DONE: created `.venv` and installed pins. Check: `.venv/bin/python -c "import numpy,pandas,sklearn;print(numpy.__version__,pandas.__version__,sklearn.__version__)"` printed `1.24.2 2.0.0 1.2.2`.
- DONE: extracted the assignment zip into `vd1/`. `sha256sum vd1/churn.csv` = `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`.
- PLAN: run the compare stage from `vd1/`: `../.venv/bin/python VD1_analysis.py compare --csv churn.csv --out outputs`.
- DONE: compare stage. Command (from `vd1/`): `../.venv/bin/python VD1_analysis.py compare --csv churn.csv --out outputs 2>&1 | tee outputs/compare_stdout.txt`, exit 0. Validation AUC: contract 0.7427, logistic 0.8384, trees 0.8456. Sizes 4225/1409/1409.
- DONE: independent checks. Command: `../.venv/bin/python check_outputs.py` printed `all checks passed` (7043x21, 1869/5174, 11 blanks at tenure 0, every source row in exactly one partition, list size 281).
- PLAN: student records validation choice in `vd1/analysis.md` and DEC-001, commit, then run evaluate with that choice.
- DONE: validation choice recorded as `trees` in `vd1/analysis.md` and DEC-001 (2026-09-28). Evaluate not yet run. Check: `ls vd1/outputs` shows no `test_metrics.csv`.
