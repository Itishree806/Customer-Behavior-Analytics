import streamlit as st
import analytics as an
import visualization as viz

st.set_page_config(page_title="Customer Segmentation", layout="wide")
st.title("🎯 Customer Segmentation")

if "df" not in st.session_state:
    st.warning("Please upload a dataset on the main page first.")
    st.stop()

df = st.session_state["df"]

st.markdown(
    "This dataset has one transaction per customer (no repeat visits), so segmentation "
    "here is based on **spend value, basket size, and age** via K-Means clustering, "
    "rather than classic RFM (which needs purchase frequency)."
)

n_clusters = st.slider("Number of segments", min_value=2, max_value=6, value=4)

with st.spinner("Running K-Means clustering..."):
    seg_df, seg_summary = an.segment_customers(df, n_clusters=n_clusters)
    st.session_state["seg_df"] = seg_df

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(viz.fig_segment_scatter(seg_df), width='stretch')
with col2:
    import plotly.express as px
    fig = px.pie(seg_summary, names="segment_name", values="total_revenue",
                 title="Revenue Share by Customer Segment", hole=0.4)
    st.plotly_chart(fig, width='stretch')

st.subheader("Segment summary")
st.dataframe(seg_summary, width='stretch')

st.subheader("Explore a segment")
chosen = st.selectbox("Select segment", seg_summary["segment_name"])
if chosen:
    st.dataframe(seg_df[seg_df["segment_name"] == chosen].head(50))