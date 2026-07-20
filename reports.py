import io
import pandas as pd
from fpdf import FPDF

import analytics as an


def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(df, seg_summary=None):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Cleaned Data", index=False)
        an.revenue_by_category(df).to_excel(writer, sheet_name="By Category", index=False)
        an.mall_performance(df).to_excel(writer, sheet_name="By Mall", index=False)
        if seg_summary is not None:
            seg_summary.to_excel(writer, sheet_name="Segments", index=False)
    return buffer.getvalue()


def to_pdf_summary_bytes(df, seg_summary=None):
    kpis = an.kpi_summary(df)
    cat = an.revenue_by_category(df)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Customer Behavior Analytics - Summary Report", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Data range: {kpis['date_range'][0]} to {kpis['date_range'][1]}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Key Metrics", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 7, f"Total Revenue: {kpis['total_revenue']:,.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Total Transactions: {kpis['total_transactions']:,}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Unique Customers: {kpis['unique_customers']:,}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Average Basket Value: {kpis['avg_basket_value']:,.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Revenue by Category", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    for _, row in cat.iterrows():
        pdf.cell(0, 7, f"{row['category']}: {row['total_revenue']:,.2f} ({int(row['transactions'])} txns)",
                  new_x="LMARGIN", new_y="NEXT")

    if seg_summary is not None:
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Customer Segments", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        for _, row in seg_summary.iterrows():
            pdf.cell(0, 7, f"{row['segment_name']}: {int(row['customers'])} customers, "
                            f"avg spend {row['avg_spend']:,.2f}", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())