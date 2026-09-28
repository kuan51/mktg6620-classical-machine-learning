# AI-use record

Tool: Claude Code (Anthropic), cloud session, 2026-09-28. Full chat export: see
`ai_use/chat_export.*` (added by the student). This file lists the prompts and what AI did.

## What AI helped with

- Set up the Python environment with the pinned versions and ran the two supplied commands unchanged.
- Explained the data checks, the three partitions, and how each method scores customers.
- Wrote `check_outputs.py` (independent asserts) and filled every table in `analysis.md` and the memo
  from the files in `outputs/`.
- Wrote `ai_use/explainer_notes.md`, plain-language notes on what each output means, which the
  student used as reference while writing.

AI did **not** write the assessed interpretations, the Q4 reasons, or the memo text. Those are the
student's own words. The validation choice was made by the student after seeing the validation table
and before the evaluate command was run.

## Prompts used (in order)

1. Opening prompt (with the handout HTML and the student files zip attached):
   > Read the assignment and follow the instructions to complete it. Interview me and ask questions
   > when a decision needs to be made, there is a fork in logic and a path needs to be chosen, or
   > closer inspection by the user would improve quality.
2. Answers to Claude's setup questions: pinned versions into `.venv`; files under `vd1/`; do not
   commit `churn.csv`; Claude fills skeletons and tables, student writes the prose.
3. Validation choice after the compare stage: `trees` (highest validation AUC); student writes the
   reason in `analysis.md`.
4. <!-- TODO(you): add any later prompts, including ones that did not work. -->

## Two checks I personally understood

<!-- TODO(you): name two checks (e.g. "no source row in two partitions", "one scenario row by calculator") and say in a sentence each what you looked at and what you saw. -->
