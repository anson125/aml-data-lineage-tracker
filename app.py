from pathlib import Path

import pandas as pd
import streamlit as st


DATA_DIR = Path(__file__).parent / "data"
TRANSACTIONS_PATH = DATA_DIR / "sample_transactions.csv"
LINEAGE_PATH = DATA_DIR / "lineage_map.csv"


st.set_page_config(
    page_title="AML Data Lineage Tracker",
    page_icon=":bar_chart:",
    layout="wide",
)


@st.cache_data
def load_transactions() -> pd.DataFrame:
    transactions = pd.read_csv(TRANSACTIONS_PATH, parse_dates=["transaction_date"])
    transactions["amount"] = transactions["amount"].astype(float)
    return transactions


@st.cache_data
def load_lineage() -> pd.DataFrame:
    return pd.read_csv(LINEAGE_PATH)


def run_quality_checks(transactions: pd.DataFrame) -> pd.DataFrame:
    checks = [
        {
            "check": "Missing customer ID",
            "status": "Pass" if transactions["customer_id"].notna().all() else "Fail",
            "records": int(transactions["customer_id"].isna().sum()),
            "business_impact": "Customer identity gaps can prevent AML alert review.",
        },
        {
            "check": "Duplicate transaction ID",
            "status": "Pass" if not transactions["transaction_id"].duplicated().any() else "Fail",
            "records": int(transactions["transaction_id"].duplicated().sum()),
            "business_impact": "Duplicate transactions can inflate monitoring volumes.",
        },
        {
            "check": "Negative or zero amount",
            "status": "Pass" if (transactions["amount"] > 0).all() else "Fail",
            "records": int((transactions["amount"] <= 0).sum()),
            "business_impact": "Invalid amounts can break scenario thresholds.",
        },
        {
            "check": "High-risk geography present",
            "status": "Review" if (transactions["risk_country"] == "High").any() else "Pass",
            "records": int((transactions["risk_country"] == "High").sum()),
            "business_impact": "High-risk country activity requires stronger review context.",
        },
        {
            "check": "Large cash movement",
            "status": "Review" if (transactions["amount"] >= 10000).any() else "Pass",
            "records": int((transactions["amount"] >= 10000).sum()),
            "business_impact": "Large movements may trigger CTR/SAR review workflows.",
        },
    ]
    return pd.DataFrame(checks)


def lineage_dot(lineage: pd.DataFrame) -> str:
    nodes = sorted(set(lineage["source_system"]).union(lineage["target_system"]))
    lines = [
        "digraph {",
        "  graph [rankdir=LR, bgcolor=transparent]",
        "  node [shape=box, style=\"rounded,filled\", fillcolor=\"#F8FAFC\", color=\"#334155\", fontname=\"Helvetica\"]",
        "  edge [color=\"#0F766E\", fontname=\"Helvetica\"]",
    ]
    for node in nodes:
        lines.append(f'  "{node}"')
    for row in lineage.itertuples(index=False):
        label = f"{row.transformation} | {row.owner}"
        lines.append(f'  "{row.source_system}" -> "{row.target_system}" [label="{label}"]')
    lines.append("}")
    return "\n".join(lines)


transactions = load_transactions()
lineage = load_lineage()
quality_checks = run_quality_checks(transactions)

st.title("AML Data Lineage Tracker")
st.caption("Trace data from source systems through transformations into an AML transaction monitoring report.")

left_filter, right_filter = st.columns([1, 1])
with left_filter:
    selected_sources = st.multiselect(
        "Source systems",
        sorted(transactions["source_system"].unique()),
        default=sorted(transactions["source_system"].unique()),
    )
with right_filter:
    selected_risk = st.multiselect(
        "Risk ratings",
        sorted(transactions["customer_risk_rating"].unique()),
        default=sorted(transactions["customer_risk_rating"].unique()),
    )

filtered = transactions[
    transactions["source_system"].isin(selected_sources)
    & transactions["customer_risk_rating"].isin(selected_risk)
]

total_volume = filtered["amount"].sum()
large_movements = int((filtered["amount"] >= 10000).sum())
review_count = int(filtered["monitoring_outcome"].eq("Review").sum())

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Transactions", f"{len(filtered):,}")
metric_2.metric("Total Volume", f"${total_volume:,.0f}")
metric_3.metric("Large Movements", f"{large_movements:,}")
metric_4.metric("AML Reviews", f"{review_count:,}")

tab_lineage, tab_quality, tab_transactions = st.tabs(
    ["Lineage", "Data Quality", "Transaction Detail"]
)

with tab_lineage:
    st.subheader("System-to-Report Lineage")
    st.graphviz_chart(lineage_dot(lineage), use_container_width=True)
    st.dataframe(
        lineage[
            [
                "source_system",
                "target_system",
                "field_name",
                "transformation",
                "owner",
                "control",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with tab_quality:
    st.subheader("Quality Control Summary")
    status_order = {"Fail": 0, "Review": 1, "Pass": 2}
    styled_checks = quality_checks.sort_values(
        by="status", key=lambda series: series.map(status_order)
    )
    st.dataframe(styled_checks, use_container_width=True, hide_index=True)

    issue_rows = quality_checks[quality_checks["status"].isin(["Fail", "Review"])]
    if not issue_rows.empty:
        st.warning(
            "Open review items detected. Use the records count and business impact fields to prioritize remediation."
        )

with tab_transactions:
    st.subheader("Monitoring Report Input")
    st.dataframe(
        filtered.sort_values("transaction_date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    by_scenario = (
        filtered.groupby("monitoring_scenario", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )
    st.bar_chart(by_scenario, x="monitoring_scenario", y="amount")
