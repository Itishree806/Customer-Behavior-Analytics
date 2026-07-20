import streamlit as st
import pandas as pd

import preprocessing as pp
import analytics as an
import visualization as viz

st.set_page_config(page_title="Customer Behavior Analytics", layout="wide", page_icon="📊")

st.title("📊 Customer Behavior Analytics Dashboard")
st.caption("Upload a customer shopping dataset to explore purchase behavior, trends, and segments.")

uploaded_file = st.file_uploader("Upload your dataset (CSV)", type="csv")

use_sample = False
if uploaded_file is None:
    use_sample = st.checkbox("No file? Use the bundled sample dataset", value=True)

if uploaded_file is not None or use_sample:
    raw_df = pd.read_csv(uploaded_file) if uploaded_file is not None else pd.read_csv("datasets/customer_shopping_data.csv")

    missing_cols = pp.validate_columns(raw_df)
    if missing_cols:
        st.error(f"Uploaded file is missing required columns: {missing_cols}")
        st.stop()

    with st.spinner("Cleaning data..."):
        df, report = pp.clean_data(raw_df)

    # session_state is how Streamlit remembers data across page switches ---
    # without this, moving to another page would forget the cleaned data.

    st.session_state["df"] = df

    st.subheader("🧹 Data Cleaning Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows (raw)", len(raw_df))
    c2.metric("Rows (cleaned)", report["final_row_count"])
    c3.metric("Duplicates removed", report["duplicates_removed"])
    c4.metric("Missing values fixed", report["missing_values_before"])

    st.divider()

    st.subheader("📈 Key Metrics")
    kpis = an.kpi_summary(df)
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Revenue", f"₺{kpis['total_revenue']:,.0f}")
    k2.metric("Transactions", f"{kpis['total_transactions']:,}")
    k3.metric("Unique Customers", f"{kpis['unique_customers']:,}")
    k4.metric("Avg Basket Value", f"₺{kpis['avg_basket_value']:,.0f}")
    k5.metric("Avg Items/Transaction", kpis["avg_items_per_transaction"])

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(viz.fig_revenue_by_category(df), width='stretch')
    with col2:
        st.plotly_chart(viz.fig_gender_split(df), width='stretch')

    with st.expander("Preview cleaned data"):
        st.dataframe(df.head(50))

else:
    st.warning("Upload a CSV file to get started, or check the sample dataset box above.")