**To:** Devon Achebe, VP of Customer Retention, Summit Telecom
**From:** Rex Linder
**Date:** September 28, 2026
**Re:** Should we pilot a model-built retention contact list?

**Recommendation**

<!-- TODO(you): one or two sentences: what Devon should do. -->

**Key numbers** (held-out test set of 1,409 customers; list = top 20%, 281 calls; Summit and these customers are a classroom example)

| | Current contract rule | Boosted-trees list |
|---|---|---|
| Real leavers among 281 calls | 112 (39.9%) | 195 (69.4%) |
| Ranking score (AUC) | 0.737 | 0.850 (+0.112, 95% interval +0.096 to +0.131) |
| Call cost for the list | $1,742.20 | $1,742.20 |
| Cost per real leaver reached | $15.56 | $8.93 |
| Save rate needed to break even | 23.6% | 13.5% |
| Net per 1,000 calls at 10% / 15% / 20% save rate | −$3,569 / −$2,254 / −$939 | −$1,620 / +$670 / +$2,960 |

Overall churn in the test set is 26.5%. Logistic regression performed about the same as boosted trees (AUC 0.847; same 195 leavers).

**Why**

<!-- TODO(you): a few sentences using the numbers above. -->

**The assumption that could reverse this**

<!-- TODO(you): name it (e.g. the true save rate) and what happens if it is wrong. -->

**How we learn whether the offer works**

<!-- TODO(you): propose the pilot or measurement (who gets the offer, who is held out, what is compared, how long). Remember a churn score is not proof the offer changes anyone's mind. -->
