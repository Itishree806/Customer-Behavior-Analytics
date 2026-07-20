import pandas as pd
import numpy as np
import preprocessing as pp
import analytics as an


def make_messy_sample():
    """A tiny fake dataset with every kind of problem a real upload could have:
    missing values, duplicates, mixed date formats, bad ages, inconsistent casing."""
    data = {
        "invoice_no": ["I001", "I002", "I002", "I003", "I004", "I005"],
        "customer_id": ["C1", "C2", "C2", "C3", None, "C5"],
        "gender": ["female", "Male", "Male", "MALE", "Female", None],
        "age": [25, 34, 34, 250, 40, -5],          # 250 and -5 are invalid ages
        "category": ["clothing", "Shoes", "Shoes", "Books", "toys", "Clothing"],
        "quantity": [2, 1, 1, 3, np.nan, 2],
        "price": [100.0, 50.0, 50.0, 20.0, 10.0, 30.0],
        "payment_method": ["cash", "Credit Card", "Credit Card", "Cash", "Debit Card", "Cash"],
        "invoice_date": ["5/8/2022", "16/05/2021", "16/05/2021", "not_a_date", "1/1/2022", "12/12/2022"],
        "shopping_mall": ["kanyon", "Metrocity", "Metrocity", "Kanyon", "Kanyon", "Metrocity"],
    }
    return pd.DataFrame(data)


def test_duplicates_removed():
    df, report = pp.clean_data(make_messy_sample())
    assert report["duplicates_removed"] >= 1
    print("PASS: duplicates removed:", report["duplicates_removed"])


def test_bad_dates_handled():
    df, report = pp.clean_data(make_messy_sample())
    assert df["invoice_date"].isnull().sum() == 0
    print("PASS: unparseable dates handled:", report["unparseable_dates_dropped"])


def test_invalid_ages_removed():
    df, report = pp.clean_data(make_messy_sample())
    assert df["age"].max() < 100 and df["age"].min() > 0
    print("PASS: invalid ages removed:", report["invalid_rows_dropped"])


def test_text_standardized():
    df, _ = pp.clean_data(make_messy_sample())
    assert set(df["gender"].unique()) <= {"Female", "Male"}
    print("PASS: text standardized:", df["gender"].unique().tolist())


def test_total_amount_correct():
    df, _ = pp.clean_data(make_messy_sample())
    row = df.iloc[0]
    assert abs(row["total_amount"] - (row["price"] * row["quantity"])) < 0.001
    print("PASS: total_amount = price * quantity")


def test_segmentation_covers_all_rows():
    df, _ = pp.clean_data(make_messy_sample())
    seg_df, seg_summary = an.segment_customers(df, n_clusters=2)
    assert seg_df["segment_name"].isnull().sum() == 0
    print("PASS: every row got assigned a segment")


def test_real_dataset_end_to_end():
    """Sanity check against your actual Kaggle dataset, not just fake data."""
    raw = pd.read_csv("datasets/customer_shopping_data.csv")
    missing = pp.validate_columns(raw)
    assert not missing, f"Real dataset missing columns: {missing}"
    df, report = pp.clean_data(raw)
    kpis = an.kpi_summary(df)
    assert kpis["total_revenue"] > 0
    print(f"PASS: real dataset end-to-end - {report['final_row_count']} clean rows, "
          f"₺{kpis['total_revenue']:,.0f} total revenue")


if __name__ == "__main__":
    tests = [
        test_duplicates_removed,
        test_bad_dates_handled,
        test_invalid_ages_removed,
        test_text_standardized,
        test_total_amount_correct,
        test_segmentation_covers_all_rows,
        test_real_dataset_end_to_end,
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            failed += 1
            print(f"FAIL: {t.__name__} -> {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed.")