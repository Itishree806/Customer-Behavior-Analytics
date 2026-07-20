import streamlit as st
import analytics as an
import reports as rp

st.set_page_config(page_title="Reports", layout="wide")
st.title("📄 Reports & Export")

if "df" not in st.session_state:
    st.warning("Please upload a dataset on the main page first.")
    st.stop()

df = st.session_state["df"]
seg_df, seg_summary = an.segment_customers(df)

st.write("Download the cleaned dataset or a generated summary report.")

col1, col2, col3 = st.columns(3)
with col1:
    st.download_button(
        "⬇️ Download Cleaned Data (CSV)",
        data=rp.to_csv_bytes(df),
        file_name="cleaned_customer_data.csv",
        mime="text/csv",
    )
with col2:
    st.download_button(
        "⬇️ Download Full Report (Excel)",
        data=rp.to_excel_bytes(df, seg_summary),
        file_name="customer_analytics_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
with col3:
    st.download_button(
        "⬇️ Download Summary (PDF)",
        data=rp.to_pdf_summary_bytes(df, seg_summary),
        file_name="summary_report.pdf",
        mime="application/pdf",
    )

st.divider()
st.subheader("Summary preview")
st.dataframe(an.revenue_by_category(df), width='stretch')
st.dataframe(seg_summary, width='stretch')