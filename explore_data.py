import pandas as pd

df = pd.read_csv("datasets/customer_shopping_data.csv")

print("SHAPE:", df.shape)
print("\nCOLUMNS:", list(df.columns))
print("\nDTYPES:\n", df.dtypes)
print("\nHEAD:\n", df.head())
print("\nNULLS PER COLUMN:\n", df.isnull().sum())
print("\nDUPLICATE ROWS:", df.duplicated().sum())
print("\nUNIQUE CUSTOMERS:", df['customer_id'].nunique(), "out of", len(df), "total rows")