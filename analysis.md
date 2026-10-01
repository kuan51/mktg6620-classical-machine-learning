# Case 1 — [Your name]

Choice record: On 9/30/2026, after seeing the validation table, I chose boosted trees because "leavers" are most likely to churn within the first quarter and the most recent months. The data set smooths out torwards a flatter curve in later quarters. This means the data is non-linear and logistic regression with tenure as a predictor would force selecting a straight line between two points on the curve.

## Q1 — Run it and describe the methods
### 1a Output

python VD1_analysis.py compare --csv churn.csv --out outputs

```text
VALIDATION RESULTS
  method    n      auc  contact_n  top20_churn_rate  top20_mean_prediction  mean_prediction  observed_churn_rate
contract 1409 0.742724        281          0.416370               0.427530         0.258283             0.265436
logistic 1409 0.838417        281          0.612100               0.650996         0.271317             0.265436
   trees 1409 0.845558        281          0.651246               0.662771         0.272776             0.265436
Highest validation AUC: trees
Record a choice and reason in analysis.md before running evaluate.
```

python VD1_analysis.py evaluate --csv churn.csv --out outputs --choice trees

```text
VALIDATION RESULTS
  method    n      auc  contact_n  top20_churn_rate  top20_mean_prediction  mean_prediction  observed_churn_rate
contract 1409 0.742724        281          0.416370               0.427530         0.258283             0.265436
logistic 1409 0.838417        281          0.612100               0.650996         0.271317             0.265436
   trees 1409 0.845558        281          0.651246               0.662771         0.272776             0.265436
Highest validation AUC: trees
FINAL TEST RESULTS
  method    n      auc  contact_n  top20_churn_rate  top20_mean_prediction  mean_prediction  observed_churn_rate
contract 1409 0.737265        281          0.398577               0.427530         0.268615             0.265436
logistic 1409 0.847207        281          0.693950               0.640176         0.273257             0.265436
   trees 1409 0.849665        281          0.693950               0.647865         0.270473             0.265436

AUC INTERVALS
             comparison  estimate       low     high
               contract  0.737265  0.716259 0.755731
               logistic  0.847207  0.825442 0.870030
                  trees  0.849665  0.828267 0.873164
logistic minus contract  0.109942  0.093153 0.128505
   trees minus contract  0.112400  0.095891 0.131117
   trees minus logistic  0.002458 -0.004875 0.010193

SCENARIOS: hypothetical dollars, not measured savings
  method  historical_list_churn_rate  assumed_save_rate  net_per_1000_contacts  break_even_save_rate
contract                    0.398577               0.10           -3569.395018              0.235687
contract                    0.398577               0.15           -2254.092527              0.235687
contract                    0.398577               0.20            -938.790036              0.235687
logistic                    0.693950               0.10           -1619.928826              0.135369
logistic                    0.693950               0.15             670.106762              0.135369
logistic                    0.693950               0.20            2960.142349              0.135369
   trees                    0.693950               0.10           -1619.928826              0.135369
   trees                    0.693950               0.15             670.106762              0.135369
   trees                    0.693950               0.20            2960.142349              0.135369
```

### 1b Methods

The contract rule looks at a single fact. The other two models look at 7 different facts and turnd it into a churn score between 0 and 1. 

The Seven Facts:
- tenure
- MonthlyCharges
- TotalCharges
- Contract
- InternetService
- Paperless Billing
- Payment Method

### 1c AI use, commands, and versions

I asked the AI to examine the difference in logic between the three models and summarize:

```
Review the python script and explain to me the difference in logic between the 3 models.
```

Response:

```
The script, VD1_analysis.py, compares three ways of scoring each customer's churn risk. They share a lot, so it helps to cover that first.

What all three share

- Same data: each method is fit on the same 60% training rows (split_rows, line 64). None of them sees validation or test outcomes while fitting.
- Same output: each produces a churn probability between 0 and 1 for every customer (predict_methods, line 94).
- Same judging: each is scored on AUC, and on the churn rate among the top 20% of customers it ranks riskiest (top_rows, line 105). This simulates contacting 20% of customers.

They differ only in how they turn a customer's attributes into a probability.

1. contract: a group-average lookup (the baseline)

fit_methods, line 77:

rates = pd.Series(y[train]).groupby(df.iloc[train]["Contract"]...).mean()                     
- It uses one column only, Contract.                                                          - "Fitting" just means computing  each contract type in the training rows. A customer's prediction is their group's rate. For example, all month-to-month customers get the same number, roughly 0.4.                                                           - If a contract type wasn't in thk to the overall churn rate(fillna(fallback)).
- Consequence: there are only 3 possible scores. Month-to-month customers are about half the base, so the top 20% is drawn entirely from one big tie. Which month-to-month customers get   picked is decided purely by tiee. The contract list is really "arandom sample of month-to-month customers."                                                 - This is the "can a spreadsheet
                                                                                              2. logistic: logistic regression

fit_methods, lines 79 and 83–89:                                                              
- It uses all 7 inputs: 3 numeric (tenure, MonthlyCharges, TotalCharges) and 4 categorical.
- Preprocessing: numeric columns are standardized and categorical columns are one-hot encoded   (one 0/1 column per category).
- The model learns one weight per input column. It adds up weight × value, then squashes the total into a probability.                                                                   - What that implies:
  - Each factor contributes independently. Being month-to-month adds the same risk whether tenure is 2 months or 60, so there are no interactions.                                            - Numeric effects run in one diays pushes risk the same way at aconstant rate on the log-odds scale. It can't learn patterns like "risk drops sharply after year 1, then flattens."
  - C=1.0 adds mild L2 regularization, which shrinks the weights slightly to reduce overfittin    This is why the scaling matte would treat columns unevenly justbecause of their units.                                                                   - It contains the contract rule atract too), plus everything else.
                                                                                              3. trees: gradient boosting (nonl

fit_methods, lines 80–81:                                                                     
GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=2)

- It uses the same 7 inputs and the same preprocessing. Trees don't need the scaling, but it d  no harm.
- It builds 100 small decision trees one after another. Each tree tries to fix the mistakes le  by the trees before it. learnincorrection small, so no single tree dominates.                                                                                  - Each tree has depth 2: it splits each branch on another. Forexample: "tenure < 6? → if yes, is InternetService = Fiber?"
- What that implies:                                                                            - Thresholds and nonlinear shap, like risk dropping after acertain tenure.
  - Two-way interactions: a factor's effect can depend on one other factor. For example, fiber customers might be high-risk only when they're also on month-to-month contracts. Depth 2      limits it to pairs, which is y.
- It is the most flexible of the three, which means it has the most capacity to find real       patterns and also the most room

Side by side

| Aspect            | contract      | logistic                     | trees              |
|-------------------|---------------|------------------------------|--------------------|
| Inputs used       | 1 (Contract)  | 7                            | 7                  |
| Distinct scores   | 3             | ~continuous                  | ~continuous   |
| Shape of effects  | group average | additive, constant direction | thresholds, curves |
| Interactions      | none          | none                         | pairwise (depth 2) |
| Interpretability  | trivial       | a coefficient per input      | harder (100 trees) |
| Overfitting risk  | lowest        | low                          | highest            |

How the choice is made
                                                                                              In main (line 217), the models arract, logistic, trees. The rankinguses a stable sort, so if two methods tie exactly on validation AUC, the simpler one is suggested.                                                                                    
The workflow is:
1. compare fits all three and reports validation results only.                                2. You record your choice in anal
3. evaluate --choice X reports test-set results.                                              
This keeps the test set from influencing which model you pick. The question the assignment is really asking: does the extra fle buy a better contact list than the one-line contract rule, by more than the bootstrap uncertainty in paired_intervals?
```

## Q2 — Is the comparison fair, and which list is better?

### 2a Data

There are 1409 customers in the file and 374 (26.5%) of them churned.

There are 11 blanks in the TotalCharges column. This is deceptive as its technically not empty and doesnt show an NA. There are also 11 customers who have a tenure of 0. Its a safe assumption that if you have a tenure of 0, you likely have not submitted any payments yet. Thus the 11 cells with empty whitespace can be imputed to 0. 

Predicting "No" is 73.5% accurate. This is not useful however, the goal is not to predict those who wont churn. Its to predict those who will churn and direct organizational resources towards retention. 

### 2b Fair test

There are 4225 rows in train and 1409 rows in validation and test. You want to measure the performance of the model against data that wasnt used to train the model. However, you also want to run a test against data that wasnt used in the validation phase. Otherwise you risk overfitting the model because its learned to predict the data that it has already seen.

### 2c The call list

| Method | Test AUC | Churn rate in its top-20% list |
| ----- | ----- | ----- |
| Contract rule	| 0.398577 |
| Logistic regression | 0.693950 |
| Boosted trees | 0.693950 |

The overall churn rate is 0.265436. Since Devon can only call 20% of the customers, he should rely on the top 20 churn rate column. This is the grouping of subscribers most likely to leave. Targeting efforts at this segment will maximize the return on retention efforts.

## Q3 — How sure are we, and is it worth money?

### 3a Uncertainty

The below table compares the boosted tree model's score to the contract score by their difference.

| AUC Estimate | CI Low | CI High |
| ----- | ------ | ----- |
| 0.112400 | 0.095891 | 0.131117 |

This table compares the Boosted Tree to the Logistic Regression model.

| AUC Estimate | CI Low | CI High |
| ----- | ------ | ----- |
| 0.002458 | -0.004875 | 0.010193 |

We are trying to compare the models to each other. Neither interval contains 0. The comparison only works if each model is measured against the same baseline. This comparison however doesnt measure uncertainty from future changes in customer behaviour. It also limits the ability of the model to generalize to a larger sample size or population.

### 3b Are the probabilities right?

The boosted trees model has a predicted mean churn rate of 0.270473 and an actual rate of 0.265436; a difference of 0.005037. The predicted churn rate for the top 20% is 0.647865 and an actual rate of 0.693950; a difference of 0.046085.

The below table is a similar comparison of the probability groups:

| Probability Group | Mean Prediction | Observed Rate | Difference |
| ----- | ------ | ----- | ----- |
| 0.0 to 0.2 | 0.0796 | 0.0718 | 0.0078 |
| 0.2 to 0.4 | 0.2978 | 0.2537 | 0.0441 |
| 0.4 to 0.6 | 0.4963 | 0.5212 | -0.0249 |
| 0.6 to 0.8 | 0.6769 | 0.6901 | -0.0132 |
| 0.8 to 1.0 | 0.8345 | 0.9143 | -0.0798 |

Prediction and reality start to diverge as the probability for the group increases. The .8 to 1.0 group has the largest differenct but only has 35 customers in it. This is too small a sample size.

### 3c Money

Net value per 1,000 contacts (from `outputs/scenarios.csv`) for the boosted tree model:

| 10% save rate | 15% save rate | 20% save rate |
|-----|-----|-----|
| −$3,569 | −$2,254 | −$939 |
| −$1,620 | $670 | $2,960 |
| −$1,620 | $670 | $2,960 |

Hand check at s = 0.15

1,000 × (r × s × $66 − $6.20)
= 1,000 × (0.693950 × 0.15 × $66 − $6.20)
= 1,000 × (0.104093 × $66 − $6.20)
= 1,000 × ($6.870107 − $6.20)
= 1,000 × $0.670107
= $670.11, which matches the CSV value of 670.107.

Break-even save rate

$6.20 ÷ (r × $66)
= $6.20 ÷ (0.693950 × $66)
= $6.20 ÷ $45.800712
= 0.135369, or about 13.5%, which matches the CSV value.

The break even rate is 13.5%. Any rate below this mark will lose money.

Below a 13.5% save rate the trees list loses money. above it, the list makes money. Logistic has the same r and gives the same figures.

The formula requires an assumption for the save rate.

## Q4 — Your choice and what would change it

### 4a Choice record

I chose boosted trees after viewing the validation outputs and before running the eval flow.

The final test did only showed a small difference between logistic regression and boosted trees. Both show a marked improvement over the contract model. The boosted trees model also slightly outperformed logistic regression on the AUC metric. This bolsters the decision to use boosted trees.

### 4b Comparison table

| Method | Test AUC | Diff vs. contract | 95% interval | Role |
|---|---|---|---|---|
| Contract rule | 0.737265 | — | 0.716259 to 0.755731 (its own AUC) | Benchmark |
| Logistic regression | 0.847207 | +0.109942 | 0.093153 to 0.128505 | Backup |
| Boosted trees | 0.849665 | +0.112400 | 0.095891 to 0.131117 | Pilot choice |

### 4c What would change my recommendation

Logistic regression showed a higher AUC.

## Q5 — Memo to Devon Achebe

To: 
Devon Achebe
VP of Customer Retention
Summit Telecom

A review of the current contract method for customer retention raised an opportunity. There are two potential supervised machine learning models that could be implemented that will drastically outperform the current contract. Logistic regression and boosted models both show a marked improvement in predicting the customers most likely to cancel their subscriptions. Retention efforts should be directed at the the top 20% of customers who these models predict will cancel.

The logistic regression model’s AUC score was 0.847 and the boosted trees score 0.850. In contrast, the current contract model is 0.737. In measuring its ability to predict customer churn, we discovered that the current contract captures ~39.9% of the top 20% of likely churners. The logistic regression model and the decision trees model both captured ~69.4%.

I recommend a pilot program of the boosted trees model. It shows a slightly better accuracy in its predictions and a pilot program should be setup to evaluate its ability to retain customers at a higher rate.

There is a caveat however, the boosted trees model assumes that it will net a customer save rate of 13.5% as this is its cost breakeven point. If the savings rate in the pilot program is beneath this rate must be considered a failure with a post mortem implemented. The target for the pilot should be a savings rate between 15% and 20%, a total savings of $670 and $2,960 per 1,000 customers. In contrast, the contract list would net losses between $939 and $3,569 per 1,000 at the same savings rate.

## AI record

Confirm that every customer in outputs/split_rows.csv shows only in a single group.

```
Yes, every customer is in exactly one group. I ran these checks on outputs/split_rows.csv:

| Check                                | Result                                                   |
|--------------------------------------|----------------------------------------------------------|
| Rows in file                         | 7,043                                                    |
| Distinct source_row values           | 7,043, so no duplicates                                  |
| source_row values                    | exactly 0 to 7,042, with no gaps                         |
| Rows with no group                   | 0                                                        |
| Rows assigned to more than one group | 0                                                        |
| Group sizes                          | train 4,225, validation 1,409, test 1,409 (sum is 7,043) |

The file identifies rows by position (source_row), not by customer ID, so I also checked against the real IDs. I matched each row to customerID in churn.csv. All 7,043 IDs are unique, and none appears in more than one group.                                                           
These numbers match the intended 60/20/20 split. They are also consistent with the assert statements in split_rows, which ccoverage every time the scriptruns.
```

Why sample both methods on the same resamples?

```
In paired_intervals (VD1_analysis.py:121), each bootstrap draw picks one random set of test customers and scores every method on that same set:

sample = rng.randint(0, len(y), size=len(y))
draws.append([roc_auc_score(y[sample], predictions[name][sample]) for name in METHODS])

The reason is that the question is about the difference between methods, and pairing measures that difference much more precisely.

1. Most of the noise comes from which customers you happen to test on

The bootstrap mimics drawing a different test set of 1,409 customers. Some test sets happen to have many easy cases, like obvious month-to-month churners. Others have many hard cases, like long-tenure customers who churned anyway.

That luck hits all methods together. On an easy sample, contract, logistic and trees all score higher. On a hard one, they all score lower. Their AUCs rise and fall together, so they are strongly positively correlated.

2. Pairing cancels the shared luck

For each draw, the code subtracts the two AUCs:

delta = draws[:, METHODS.index(a)] - draws[:, METHODS.index(b)]

The "easy sample" bonus appears in both AUCs, so it cancels out. What's left is mostly the part that actually differs: how the two methods rank the same customers differently.

In formula terms:

Var(A − B) = Var(A) + Var(B) − 2·Cov(A, B)

Because Cov(A, B) is large and positive here, the variance of the difference is much smaller than either AUC's variance alone.

3. Unpaired resampling would answer a different, noisier question

If each method got its own independent resamples, the covariance term would be zero. Then:

- The
5. Fairness

Pairing also means every comparison is on equal terms. In each draw, both methods face exactly the same customers with exactly the same outcomes. No method gets an easier set of customers by chance.

What the pairing doesn't cover

The docstring says this, but it's worth repeating. Predictions are fixed, and only the evaluation rows are resampled. The intervals capture uncertainty from which test customers you happened to get. They don't capture uncertainty from:

- refitting the models on different training data
- your validation-stage choice
- future drift in customer behaviour
- whether contacting customers actually changes churn
```

Using outputs/scenarios.csv, calculate the list turn rate for the boosted trees model and calculate the 10, 15, and 20% rates.

```
For the boosted trees model, the list churn rate is 69.4%. I'm reading "turn" as "churn". That's 195 of the 281 test customers the model ranked in its top 20% who actually churned (outputs/test_metrics.csv).

The script's formula for the dollar figures is 1000 x (churn_rate x save_rate x $66 - $6.20) (VD1_analysis.py:165). I recomputed each value by hand and they match the CSV:

| Assumed save rate | Customers saved per contact (0.694 x rate) | Net per 1,000 contacts |
|-------------------|--------------------------------------------|------------------------|
| 10%               | 0.0694                                     | -$1,619.93             |
| 15%               | 0.1041                                     | +$670.11               |
| 20%               | 0.1388                                     | +$2,960.14             |

- Break-even save rate is 13.5% ($6.20 / (0.694 x $66)). At 10% the campaign loses money. At 15% and above it makes money.
- Trees and logistic regression give identical figures. Both models had exactly 195 churners in their 281-customer lists. The lists may hold different customers, but the churn rate is the same, so every dollar figure is too.
- These are hypothetical dollars, not measured savings. As the script notes, the save rates are assumptions and no treatment effect was estimated.
```