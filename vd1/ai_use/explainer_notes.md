# Explainer notes (written by AI, for study only; not submitted as assessed writing)

These notes were written by Claude to help the student understand the output. They cover the
**validation** results only (1,409 customers), from `outputs/validation.csv` plus the same script
re-run in memory. Final-test numbers replace them once `evaluate` runs. Money figures here are a
preview; the assignment's value scenarios must use the final-test list.

## The story in one breath

The company can call 281 of 1,409 customers. Three ways of picking those 281 were tried. The best
found a group where about 2 in 3 were really about to leave; random picking finds about 1 in 4.
Whether calling them pays depends on the save rate s: how many leavers the offer actually keeps.
The data do not tell us s.

## The three methods

- **Contract rule.** Score = the training churn rate for the customer's contract type:
  month-to-month 42.8%, one year 10.3%, two year 3.3%. The validation pile has 752 month-to-month
  customers, all tied at the same score, so the 281-call list is a fixed random draw from them.
  That is why its list churn rate (41.6%) is close to the month-to-month rate.
- **Logistic regression.** One weight per input, added up and turned into a probability.
- **Boosted trees.** 100 small depth-2 trees, each correcting the previous ones. Can pick up
  combinations of inputs that a single weighted sum misses.

## Scoreboard (validation)

| | Contract rule | Logistic | Trees |
|---|---|---|---|
| AUC (ranking score) | 0.743 | 0.838 | 0.846 |
| Calls made (top 20%) | 281 | 281 | 281 |
| Cost per call | $6.20 | $6.20 | $6.20 |
| Total call cost (281 × $6.20) | $1,742.20 | $1,742.20 | $1,742.20 |
| Real leavers reached | 117 | 172 | 183 |
| Share of list who really left | 41.6% | 61.2% | 65.1% |
| Cost per real leaver reached | $14.89 | $10.13 | $9.52 |
| Times better than random (26.5%) | 1.57× | 2.31× | 2.45× |
| Model's average guess for its list | 42.8% | 65.1% | 66.3% |
| Model's average guess for everyone (actual 26.5%) | 25.8% | 27.1% | 27.3% |

How to read it:
- **AUC**: pick one leaver and one stayer at random; AUC is how often the leaver gets the higher
  score. 0.5 = coin flip. It measures ordering, not "percent correct".
- **Real leavers reached / cost per leaver**: every list costs the same, so the better list is the
  one whose calls land on more real leavers.
- **Guess vs reality (calibration)**: logistic guessed 65.1% for its list, 61.2% left (a bit
  overconfident). Trees guessed 66.3%, 65.1% left. A correct overall average does not prove each
  group is right; the final test's probability groups check that.
- The list holds people most likely to **leave**. Nothing here shows that calling them makes them stay.

## The two comparisons

- **Models vs contract rule**: about +0.10 AUC and 55–66 more real leavers on the same list. Large.
- **Trees vs logistic**: +0.007 AUC and 11 more leavers out of 281. Small; could be luck of the
  split. The final test's paired bootstrap intervals show whether each difference clearly excludes zero.

## Money preview for the 281-call list

Net = leavers reached × s × $66 − $1,742.20. Same as 1,000 × (r × s × $66 − $6.20) scaled by 0.281.

| Method | s = 10% | s = 15% | s = 20% | Break-even s = $6.20 / (r × $66) |
|---|---|---|---|---|
| Contract | −$970.00 | −$583.90 | −$197.80 | 22.6% |
| Logistic | −$607.00 | −$39.40 | +$528.20 | 15.3% |
| Trees | −$534.40 | +$69.50 | +$673.40 | 14.4% |

Worked example, trees at 15%: 183 × 0.15 = 27.45 saved × $66 = $1,811.70 − $1,742.20 = +$69.50.
Cost per leaver ÷ $66 = break-even s (trees: $9.52 / $66 ≈ 14.4%).

## Still unknown

- Validation numbers will differ from test numbers; the test numbers count.
- Public example data, not Summit's; a future campaign may differ.
- High churn risk is not the same as persuadable. Learning s needs a randomized test:
  offer half the list, hold out the other half, compare retention.

## Self-test questions

1. Why is "real leavers reached" more useful to Devon than AUC?
2. Why is the contract rule's list churn rate almost the month-to-month rate?
3. At s = 12%, which methods lose money?
4. What would a trees-minus-logistic interval that crosses zero tell you?

---

# Final-test results (added after `evaluate --choice trees`)

| | Contract rule | Logistic | Trees (chosen) |
|---|---|---|---|
| Final-test AUC | 0.737 | 0.847 | 0.850 |
| Real leavers among 281 calls | 112 | 195 | 195 |
| Share of list who left | 39.9% | 69.4% | 69.4% |
| Cost per real leaver ($1,742.20 / leavers) | $15.56 | $8.93 | $8.93 |
| Break-even save rate | 23.6% | 13.5% | 13.5% |

What changed from validation, in plain words:
- **Logistic caught up.** On validation, trees found 11 more leavers. On test, both lists find exactly
  195. The lists are not identical: 234 of 281 customers are on both. The ranking gap is tiny
  (+0.0025 AUC), and its interval, −0.005 to +0.010, includes zero. So the test cannot say which model
  ranks better. It also does not prove they are equal.
- **Both models clearly beat the old rule.** Trees minus contract is +0.112, with an interval of
  +0.096 to +0.131. The whole range is above zero.
- **Pairing, simply put.** Each of the 1,000 bootstrap rounds draws one random sample of test customers
  (with repeats) and scores both methods on the same sample. The difference is taken inside each round,
  so luck in which customers were drawn hits both methods equally and mostly cancels out.
- **Calibration for trees.** Overall it guesses 27.0% against 26.5% observed, which is close. Inside the list
  it guesses 64.8% against 69.4% observed, so it under-guesses by about 5 points. In the 0.2–0.4 group it
  guesses 29.8% against 25.4% observed, so it over-guesses a bit. The top group, 0.8 to 1.0, has only 35
  people (about 32 leavers), too few to judge.
- **Money.** The test list is better than the validation list (69.4% vs 65.1%), so break-even drops to
  13.5%. It is still negative at a 10% save rate and positive at 15% and 20%. The recommendation hinges
  on a save rate the data cannot estimate.
