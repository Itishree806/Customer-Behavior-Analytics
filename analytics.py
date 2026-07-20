import pandas as pd


def kpi_summary(df):
    return {
        "total_revenue": round(df["total_amount"].sum(), 2),
        "total_transactions": len(df),
        "unique_customers": df["customer_id"].nunique(),
        "avg_basket_value": round(df["total_amount"].mean(), 2),
        "avg_items_per_transaction": round(df["quantity"].mean(), 2),
        "date_range": (str(df["invoice_date"].min().date()), str(df["invoice_date"].max().date())),
    }


def revenue_by_category(df):
    return (
        df.groupby("category")["total_amount"]
        .agg(total_revenue="sum", transactions="count", avg_value="mean")
        .sort_values("total_revenue", ascending=False)
        .reset_index()
    )


def gender_breakdown(df):
    return df.groupby("gender")["total_amount"].agg(
        total_revenue="sum", transactions="count", avg_spend="mean"
    ).reset_index()


def age_group_breakdown(df):
    return df.groupby("age_group", observed=True)["total_amount"].agg(
        total_revenue="sum", transactions="count", avg_spend="mean"
    ).reset_index()


def mall_performance(df):
    return (
        df.groupby("shopping_mall")["total_amount"]
        .agg(total_revenue="sum", transactions="count")
        .sort_values("total_revenue", ascending=False)
        .reset_index()
    )



from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def segment_customers(df, n_clusters=4):
    features = df[["total_amount", "quantity", "price", "age"]].copy()

    # K-Means is distance-based, so features on different scales (price in
    # thousands, age in tens) would unfairly dominate. Scaling puts them
    # all on a comparable footing first.
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(scaled)

    out = df.copy()
    out["segment"] = labels

    # KMeans gives arbitrary cluster numbers (0,1,2,3) with no inherent order.
    # We rank them by avg spend so the labels are meaningful business terms.
    seg_avg = out.groupby("segment")["total_amount"].mean().sort_values()
    rank_map = {seg: rank for rank, seg in enumerate(seg_avg.index)}
    tier_names = ["Budget Shoppers", "Occasional Spenders", "Regular Spenders", "High-Value Shoppers"]
    name_map = {seg: tier_names[min(rank, len(tier_names)-1)] for seg, rank in rank_map.items()}
    out["segment_name"] = out["segment"].map(name_map)

    summary = out.groupby("segment_name").agg(
        customers=("customer_id", "nunique"),
        avg_spend=("total_amount", "mean"),
        avg_quantity=("quantity", "mean"),
        avg_age=("age", "mean"),
        total_revenue=("total_amount", "sum"),
    ).sort_values("avg_spend", ascending=False).reset_index()

    return out, summary



if __name__ == "__main__":
    df = pd.read_csv("datasets/cleaned_customer_shopping_data.csv", parse_dates=["invoice_date"])

    print("=== KPI SUMMARY ===")
    print(kpi_summary(df))

    print("\n=== REVENUE BY CATEGORY ===")
    print(revenue_by_category(df))

    print("\n=== GENDER BREAKDOWN ===")
    print(gender_breakdown(df))

    print("\n=== AGE GROUP BREAKDOWN ===")
    print(age_group_breakdown(df))

    print("\n=== MALL PERFORMANCE ===")
    print(mall_performance(df))

    print("\n=== CUSTOMER SEGMENTATION ===")
    seg_df, seg_summary = segment_customers(df)

    print(seg_summary)
    
    seg_df.to_csv("datasets/segmented_customer_data.csv", index=False)
    print("\nSaved segmented_customer_data.csv")