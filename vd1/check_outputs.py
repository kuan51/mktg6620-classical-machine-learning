"""Independent checks on churn.csv and outputs/. Run from vd1/: ../.venv/bin/python check_outputs.py"""
import math, os
import pandas as pd

df = pd.read_csv("churn.csv")
assert df.shape == (7043, 21), df.shape
assert df["Churn"].value_counts().to_dict() == {"No": 5174, "Yes": 1869}
assert df["customerID"].is_unique
blank = df["TotalCharges"].astype(str).str.strip().eq("")
assert blank.sum() == 11 and (df.loc[blank, "tenure"] == 0).all()
print("data: 7043x21, 1869 Yes / 5174 No, 11 blank TotalCharges all at tenure 0")

split = pd.read_csv("outputs/split_rows.csv")
assert split["source_row"].is_unique and len(split) == 7043            # each row in exactly one partition
sizes = split["partition"].value_counts().to_dict()
assert sizes == {"train": 4225, "validation": 1409, "test": 1409}, sizes
assert math.floor(0.20 * 1409) == 281                                  # contact list size
print("split: every source row appears once;", sizes, "; top-20% list = 281 rows")

if os.path.exists("outputs/test_metrics.csv"):
    m = pd.read_csv("outputs/test_metrics.csv").set_index("method")
    s = pd.read_csv("outputs/scenarios.csv")
    for row in s.itertuples():
        r = m.loc[row.method, "top20_churn_rate"]
        assert abs(row.historical_list_churn_rate - r) < 1e-12
        assert abs(row.net_per_1000_contacts - 1000 * (r * row.assumed_save_rate * 66 - 6.20)) < 1e-6
        assert abs(row.break_even_save_rate - 6.20 / (r * 66)) < 1e-12
    print("scenarios: all", len(s), "rows recompute from r*s*66-6.20 and 6.20/(r*66)")
print("all checks passed")
