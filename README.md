# Customer Behavior Analytics Dashboard

An interactive Streamlit dashboard that turns raw retail transaction
data into customer behavior insights — purchase trends, category
performance, and data-driven customer segments.

## Dataset

**Source:** Customer Shopping Dataset – Retail Sales Data (Kaggle),
by Mehmet Tahir Aslan.

99,457 transactions from 10 shopping malls in Istanbul (Jan 2021 – Mar 2023).

> **Note:** each 'customer_id' appears exactly once in this dataset
> (no repeat customers), so segmentation is done on spend value,
> basket size, and age via K-Means — not classic RFM, which requires
> purchase frequency.

## Features

- **Upload & Clean** — handles missing values, duplicates, mixed date
  formats, and invalid values automatically.
- **Overview** — key metrics and monthly sales trend.
- **Purchase Analysis** — trends, payment methods, mall performance,
  date-range filtering.
- **Product Category** — category revenue, and breakdowns by gender
  and age group.
- **Customer Segmentation** — K-Means clustering into value tiers,
  adjustable cluster count.
- **Reports** — one-click export to CSV, Excel, and PDF.

## Project Structure

Customer-Behavior-Analytics/
├── app.py
├── preprocessing.py
├── analytics.py
├── visualization.py
├── reports.py
├── tests.py
├── pages/
│   ├── 1_Purchase_Analysis.py
│   ├── 2_Product_Category.py
│   ├── 3_Customer_Segmentation.py
│   └── 4_Reports.py
├── datasets/
├── outputs/
└── requirements.txt

## Setup & Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Testing

```bash
python tests.py
```

## Tech Stack

Python, Streamlit, Pandas, NumPy, Plotly, Matplotlib,
Scikit-learn (K-Means), OpenPyXL, fpdf2

## Author

Itishree Sahoo — Data Analytics Project (March Batch), Bleep Education 