import plotly.express as px
import pandas as pd
import analytics as an


def fig_revenue_by_category(df):
    cat = an.revenue_by_category(df)
    return px.bar(cat, x="category", y="total_revenue", color="category",
                  title="Revenue by Product Category")


def fig_gender_split(df):
    gender = an.gender_breakdown(df)
    return px.pie(gender, names="gender", values="total_revenue",
                  title="Revenue Share by Gender", hole=0.4)


def fig_age_group_spend(df):
    age = an.age_group_breakdown(df)
    return px.bar(age, x="age_group", y="avg_spend", color="age_group",
                  title="Average Spend by Age Group")


def fig_mall_performance(df):
    mall = an.mall_performance(df)
    fig = px.bar(mall, x="shopping_mall", y="total_revenue",
                 title="Revenue by Shopping Mall")
    fig.update_layout(xaxis_tickangle=-35)
    return fig


def fig_segment_scatter(seg_df):
    # Plotting all 99,457 points is slow to render interactively in-browser.
    # We sample for the VISUAL only — the clustering itself already ran on full data.
    sample = seg_df.sample(n=min(3000, len(seg_df)), random_state=42)
    return px.scatter(sample, x="age", y="total_amount", color="segment_name",
                       title="Customer Segments: Age vs Spend (sampled for display)", opacity=0.6)



if __name__ == "__main__":
    import os
    df = pd.read_csv("datasets/cleaned_customer_shopping_data.csv", parse_dates=["invoice_date"])
    seg_df, seg_summary = an.segment_customers(df)

    os.makedirs("outputs/charts", exist_ok=True)

    charts = {
        "revenue_by_category": fig_revenue_by_category(df),
        "gender_split": fig_gender_split(df),
        "age_group_spend": fig_age_group_spend(df),
        "mall_performance": fig_mall_performance(df),
        "segment_scatter": fig_segment_scatter(seg_df),
    }

    for name, fig in charts.items():
        path = f"outputs/charts/{name}.html"
        fig.write_html(path)
        print("Saved:", path)