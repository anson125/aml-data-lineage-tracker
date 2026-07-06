# AML Data Lineage Tracker

This is a small Streamlit app I built to show how AML transaction data can move from different source systems into a final monitoring report.

The goal was to make data lineage easier to understand at a glance: where the data starts, what happens to it, who owns each step, and what checks help make the reporting more reliable.

## What This Includes

- A visual flow from source systems to the AML monitoring report
- A simple lineage table showing fields, transformations, owners, and controls
- Sample transaction data for AML review scenarios
- Data quality checks for missing IDs, duplicate transaction IDs, invalid amounts, high-risk countries, and large transactions
- Filters for source systems and customer risk ratings
- A transaction detail view with a basic scenario chart

## Tech Stack

- Python
- Streamlit
- Pandas
- CSV sample datasets

## Project Structure

```text
.
|-- app.py
|-- data
|   |-- lineage_map.csv
|   `-- sample_transactions.csv
|-- requirements.txt
`-- README.md
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Why I Built It

In banking and compliance work, it is not enough to only have the final report. Teams also need to understand how the data got there. This project is a simple version of that idea, focused on AML monitoring data.

I wanted this to show a mix of data analysis, documentation, and business context. The app is intentionally lightweight, but it covers the kind of questions data governance and financial crimes teams usually care about:

- What system did the data come from?
- Which fields were transformed?
- Who owns each step?
- What controls are in place?
- Are there quality issues that need review?

## Next Things I May Add

- Add Excel upload support for custom lineage maps
- Add a download option for quality check results
- Add more AML scenarios, like structuring or rapid movement of funds
- Add screenshots after deployment
- Deploy with Streamlit Community Cloud
