# V&D Project 1 — Case 1: Which customers should the retention team contact?

MKTG 6620, Fall 2026. Compares a contract-rule baseline with logistic regression and boosted trees
for building a top-20% retention contact list, using the supplied `VD1_analysis.py` unchanged.

## Files

- `VD1_STUDENT_PACK.html` — the assignment handout.
- `VD1_analysis.py`, `VD1_requirements.txt` — instructor-supplied script and pins (unchanged).
- `check_outputs.py` — small independent asserts on the data, the partitions and the scenario arithmetic.
- `outputs/` — every file the two commands wrote, plus the console output of each run (`*_stdout.txt`).
- `analysis.md` — Q1–Q4 write-up. `memo.md` / `memo.pdf` — one-page memo to Devon Achebe.
- `ai_use/` — AI-use record: prompts, the chat export, and notes on what AI helped with.

## Data

`churn.csv` is the course copy of the public Telco churn example and is **not committed**.
Download it from the Canvas assignment package and place it in this folder. The run records in
`outputs/*_run.json` carry its SHA-256 (`16320c9c…3055e91`) so the grader can confirm the same file.

Source note (kept per the handout): Telco churn dataset mirror,
https://huggingface.co/datasets/scikit-learn/churn-prediction, declared CC BY 4.0 (checked by the
instructor September 9, 2026). `Churn = Yes` means the customer left. Summit Telecom and Devon Achebe
are fictional; the data are a classroom example, not company records.

## Setup

Python 3.11. From the repo root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r vd1/VD1_requirements.txt
```

Versions actually used are recorded automatically in `outputs/compare_run.json` and
`outputs/evaluate_run.json` (numpy 1.24.2, pandas 2.0.0, scikit-learn 1.2.2, Python 3.11.15).

## The two commands

Run from inside `vd1/`:

```bash
../.venv/bin/python VD1_analysis.py compare  --csv churn.csv --out outputs
../.venv/bin/python VD1_analysis.py evaluate --csv churn.csv --out outputs --choice trees
```

**Recorded choice:** `trees` (boosted trees), chosen from the validation table on 2026-09-28 before
`evaluate` was run. See the top of `analysis.md`.

Optional check: `../.venv/bin/python check_outputs.py` should print `all checks passed`.

## Building the memo PDF

From the repo root, after `.venv/bin/pip install markdown`:

```bash
{ echo '<html><head><meta charset="utf-8"><style>body{font-family:Arial;font-size:10.5pt}table{border-collapse:collapse}td,th{border:1px solid #888;padding:2px 6px}</style></head><body>'; .venv/bin/python -m markdown -x tables vd1/memo.md; echo '</body></html>'; } > vd1/memo.html
chromium --headless --no-sandbox --no-pdf-header-footer --print-to-pdf=vd1/memo.pdf file://$PWD/vd1/memo.html
```
