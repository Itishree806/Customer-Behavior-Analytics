import streamlit as st
import analytics as an
import visualization as viz

st.set_page_config(page_title="Product Category", layout="wide")
st.title("🏷️ Product Category Insights")

if "df" not in st.session_state:
    st.warning("Please upload a dataset on the main page first.")
    st.stop()

df = st.session_state["df"]

st.plotly_chart(viz.fig_revenue_by_category(df), width='stretch')

st.subheader("Category performance table")
st.dataframe(an.revenue_by_category(df), width='stretch')

st.subheader("Who buys what? Category by gender")
cross = df.groupby(["category", "gender"])["total_amount"].sum().unstack().fillna(0)
st.bar_chart(cross)

st.subheader("Category by age group")
cross_age = df.groupby(["category", "age_group"], observed=True)["total_amount"].sum().unstack().fillna(0)
st.bar_chart(cross_age)