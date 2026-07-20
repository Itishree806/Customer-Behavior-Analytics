import pandas as pd

REQUIRED_COLUMNS = [
    "invoice_no", "customer_id", "gender", "age", "category",
    "quantity", "price", "payment_method", "invoice_date", "shopping_mall"
]


def validate_columns(df):
    """Return list of required columns missing from the uploaded file."""
    return [c for c in REQUIRED_COLUMNS if c not in df.columns]


def clean_data(df):
    report = {}
    df = df.copy()

    # 1. Missing values
    report["missing_values_before"] = int(df.isnull().sum().sum())
    for col in ["age", "quantity", "price"]:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    for col in ["gender", "category", "payment_method", "shopping_mall"]:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])
    before = len(df)
    df = df.dropna(subset=["customer_id", "invoice_date"])
    report["rows_dropped_missing_ids"] = before - len(df)

    # 2. Duplicates
    report["duplicates_removed"] = int(df.duplicated().sum())
    df = df.drop_duplicates()

    # 3. Fix data types — in DD/MM/YYYY format
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], dayfirst=True, errors="coerce")
    report["unparseable_dates_dropped"] = int(df["invoice_date"].isnull().sum())
    df = df.dropna(subset=["invoice_date"])

    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # 4. Standardize text casing (so "male", "Male", "MALE" don't get counted separately)
    for col in ["gender", "category", "payment_method", "shopping_mall"]:
        df[col] = df[col].astype(str).str.strip().str.title()

    # 5. Drop impossible values
    before = len(df)
    df = df[(df["age"] > 0) & (df["age"] < 100)]
    df = df[(df["price"] > 0) & (df["quantity"] > 0)]
    report["invalid_rows_dropped"] = before - len(df)

    # 6. Derived columns 
    df["total_amount"] = df["price"] * df["quantity"]
    df["month"] = df["invoice_date"].dt.to_period("M").astype(str)
    df["age_group"] = pd.cut(
        df["age"], bins=[17, 25, 35, 45, 55, 100],
        labels=["18-25", "26-35", "36-45", "46-55", "56+"]
    )

    report["final_row_count"] = len(df)
    return df, report


if __name__ == "__main__":
    raw = pd.read_csv("datasets/customer_shopping_data.csv")
    missing = validate_columns(raw)
    if missing:
        print("Missing required columns:", missing)
    else:
        clean_df, rep = clean_data(raw)
        print("Cleaning report:", rep)
        clean_df.to_csv("datasets/cleaned_customer_shopping_data.csv", index=False)
        print("Saved cleaned file with shape:", clean_df.shape)