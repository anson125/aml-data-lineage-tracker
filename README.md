# AML Data Lineage Tracker

An interactive Streamlit project that shows how transaction data moves from source systems into an AML transaction monitoring report. It is designed as a portfolio-ready example of data lineage, control mapping, and data quality review in a financial-crimes context.

## What It Shows

- Source-to-report lineage for AML monitoring data
- Field-level transformations and ownership
- Sample quality checks for missing IDs, duplicate transactions, invalid amounts, high-risk geography, and large movements
- Filterable transaction monitoring input data
- A visual lineage graph from source systems to the final AML monitoring report

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

## Portfolio Context

This project simulates the kind of lineage documentation used by banking, compliance, data governance, and AML teams. The goal is to make it easy to explain where data comes from, which transformations occur, who owns each step, and which controls support trusted reporting.

## Possible Next Enhancements

- Add Excel upload support for custom lineage maps
- Add downloadable quality check results
- Add more AML scenarios such as structuring, rapid movement of funds, and high-risk counterparty activity
- Add screenshots to the README after deploying the app
- Deploy with Streamlit Community Cloud
