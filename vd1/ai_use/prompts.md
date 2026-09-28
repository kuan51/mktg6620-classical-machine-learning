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
4. Asked for "sentences interpreting the results that I can use as inspiration". Claude declined to
   draft them (course policy) and instead explained what each column of the validation table means.
5. The handout's starting prompt, pasted verbatim after compare had already run:
   > Read the Case 1 handout and VD1_analysis.py. Use the local churn.csv. Run the compare stage with
   > the supplied settings. Explain the data checks, the three partitions, and how each method makes
   > predictions. Show the validation table. Do not run the final evaluation until I record my choice.
   > Help me understand the output, but do not write my assessed explanations or decision memo.
6. "help me I dont understand this assignment or what its doing" — Claude gave a plain-language
   overview of the business problem, the three partitions and the three methods.
7. "What is the difference between list churn rate and observed churn rate? And between list mean
   prediction and mean prediction?" — Claude explained actual vs predicted, list vs everyone.
8. "Give me a full report walking through the findings and comparisons so I can study the results.
   Explain like im 5." — Claude wrote the study report saved as `explainer_notes.md`.
9. "Update the report matrix to include a cost estimate using the $6.20 per call and the total cost
   for each model." — Claude added total call cost (281 × $6.20 = $1,742.20) and cost per real leaver.
10. Student sent a first draft of the validation reason. Claude did not rewrite it; it listed four
    factual problems (single decision tree vs boosted trees; the list selects likely leavers, not
    stayers; retention depends on the unknown save rate; the AUC rule was not cited). The student
    chose to revise it in their own words.
11. Second draft of the reason. Claude listed remaining unsupported claims (models do not reduce churn;
    the list still holds stayers; retention depends on the offer; AUC is not return on investment;
    length). The student revised again.
12. Third draft. The student kept the AUC/return-on-investment sentence; Claude recorded the text
    verbatim in `analysis.md`, committed it, then ran `evaluate --choice trees`.
13. "Help me understand how the boosted tree and logistic regression affect churn" (quoting the Q1 TODO).
    Claude corrected the premise (the methods score risk; they do not change churn) and showed the
    fitted logistic weights, tree input usage and two example customers.
14. Student sent a Q1 draft. Claude listed four factual errors (cause and effect in the contract rule,
    no input selection in logistic, 0-1 applies to the output, trees do not resample churners). The
    student revised it and asked why the methods share the same inputs; Claude explained (fair
    comparison, same information). On the second draft Claude flagged two remaining points (same
    inputs vs same baseline; "improves outcomes"); the student chose to record it as written.
15. <!-- TODO(you): add any later prompts, including ones that did not work. -->

## Two checks I personally understood

<!-- TODO(you): name two checks (e.g. "no source row in two partitions", "one scenario row by calculator") and say in a sentence each what you looked at and what you saw. -->
