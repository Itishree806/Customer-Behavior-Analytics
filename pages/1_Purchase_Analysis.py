import streamlit as st
import analytics as an
import visualization as viz

st.set_page_config(page_title="Purchase Analysis", layout="wide")
st.title("🛒 Purchase Analysis")

if "df" not in st.session_state:
    st.warning("Please upload a dataset on the main page first.")
    st.stop()

df = st.session_state["df"]

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(viz.fig_age_group_spend(df), width='stretch')
with col2:
    st.plotly_chart(viz.fig_mall_performance(df), width='stretch')

st.subheader("Filter by date range")
min_date, max_date = df["invoice_date"].min(), df["invoice_date"].max()
date_range = st.date_input("Select range", (min_date, max_date), min_value=min_date, max_value=max_date)

if len(date_range) == 2:
    mask = (df["invoice_date"] >= str(date_range[0])) & (df["invoice_date"] <= str(date_range[1]))
    filtered = df[mask]
    st.write(f"{len(filtered):,} transactions in selected range · Revenue: ₺{filtered['total_amount'].sum():,.0f}")
    st.dataframe(filtered.head(100))