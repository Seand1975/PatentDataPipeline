import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px   # ✅ ADD THIS

# -----------------------------
# DB CONNECTION
# -----------------------------
DB_URL = "postgresql+psycopg2://postgres:bottonse@localhost:5432/patents_db"
engine = create_engine(DB_URL)

st.set_page_config(page_title="Patent Analytics Dashboard", layout="wide")

st.title("📊 Patent Analytics Dashboard")



# -----------------------------
# QUERY FUNCTION
# -----------------------------
def run_query(query):
    return pd.read_sql(query, engine)


# -----------------------------
# KPI STATS (FIXED FOR YOUR SCHEMA)
# -----------------------------
st.subheader("📌 Key Statistics")

kpi_query = """
SELECT
    COUNT(*) AS total_patents,
    MIN(filing_date) AS min_date,
    MAX(filing_date) AS max_date,
    COUNT(DISTINCT o.level_one) AS total_organizations,
    COUNT(DISTINCT p.foreign_country_filed) AS total_countries
FROM patents_priority p
LEFT JOIN patents_orgs o
ON p.patent_id = o.patent_id;
"""

kpi_df = run_query(kpi_query)

# Extract values safely
total_patents = int(kpi_df["total_patents"][0] or 0)

min_date = kpi_df["min_date"][0]
max_date = kpi_df["max_date"][0]

min_year = min_date.year if pd.notnull(min_date) else 0
max_year = max_date.year if pd.notnull(max_date) else 0

total_orgs = int(kpi_df["total_organizations"][0] or 0)
total_countries = int(kpi_df["total_countries"][0] or 0)

# Display
col1, col2, col3, col4 = st.columns(4)

col1.metric("📊 Total Patents", f"{total_patents:,}")
col2.metric("📅 Year Range", f"{min_year} - {max_year}")
col3.metric("🏢 Organizations", f"{total_orgs:,}")
col4.metric("🌍 Countries", f"{total_countries:,}")
# -----------------------------
# SIDEBAR MENU
# -----------------------------
menu = st.sidebar.selectbox(
    "Select Analysis",
    [
        "Top Organizations",
        "Top Countries",
        "Patent Trends Over Time",
        "Most Active Agencies",
        "Full JOIN View",
        "Ranking (Window Function)"
    ]
)

# -----------------------------
# Q1: TOP ORGANIZATIONS
# -----------------------------
if menu == "Top Organizations":
    st.subheader("🏢 Top Organizations by Patents")

    query = """
    SELECT level_one, COUNT(*) AS total_patents
    FROM patents_orgs
    GROUP BY level_one
    ORDER BY total_patents DESC
    LIMIT 20;
    """

    df = run_query(query)

    st.dataframe(df)

    # Bar chart
    st.subheader("Bar Chart")
    st.bar_chart(df.set_index("level_one"))

    # ✅ Plotly Pie Chart (RESTORED)
    st.subheader("Pie Chart")
    fig = px.pie(df, names="level_one", values="total_patents", title="Organization Share")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Q2: TOP COUNTRIES
# -----------------------------
elif menu == "Top Countries":
    st.subheader("🌍 Countries with Most Patents")

    query = """
    SELECT foreign_country_filed, COUNT(*) AS total
    FROM patents_priority
    GROUP BY foreign_country_filed
    ORDER BY total DESC
    LIMIT 20;
    """

    df = run_query(query)

    st.dataframe(df)

    # Bar chart
    st.subheader("Bar Chart")
    st.bar_chart(df.set_index("foreign_country_filed"))

    # ✅ Plotly Pie Chart
    st.subheader("Pie Chart")
    fig = px.pie(df, names="foreign_country_filed", values="total", title="Country Share")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Q3: TRENDS OVER TIME
# -----------------------------
elif menu == "Patent Trends Over Time":
    st.subheader("📈 Patent Filings Over Time")

    query = """
    SELECT EXTRACT(YEAR FROM filing_date) AS year, COUNT(*) AS total
    FROM patents_priority
    WHERE filing_date IS NOT NULL
    GROUP BY year
    ORDER BY year;
    """

    df = run_query(query)

    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    df = df.sort_values("year")

    st.dataframe(df)

    # Line chart
    st.subheader("Line Chart")
    st.line_chart(df.set_index("year"))

    # Scatter plot
    st.subheader("Scatter Plot")
    fig, ax = plt.subplots()
    ax.scatter(df["year"], df["total"])
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Patents")
    st.pyplot(fig)

# -----------------------------
# Q4: MOST ACTIVE AGENCIES
# -----------------------------
elif menu == "Most Active Agencies":
    st.subheader("🏛️ Most Active Government Agencies")

    query = """
    SELECT fedagency_name, COUNT(*) AS total
    FROM patents_orgs
    GROUP BY fedagency_name
    ORDER BY total DESC
    LIMIT 20;
    """

    df = run_query(query)

    st.dataframe(df)

    # Bar chart
    st.subheader("Bar Chart")
    st.bar_chart(df.set_index("fedagency_name"))

    # ✅ Plotly Pie Chart
    st.subheader("Pie Chart")
    fig = px.pie(df, names="fedagency_name", values="total", title="Agency Share")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Q5: JOIN VIEW + HEATMAP
# -----------------------------
elif menu == "Full JOIN View":
    st.subheader("🔗 Patents + Organizations (JOIN)")

    query = """
    SELECT 
        p.patent_id,
        o.fedagency_name,
        o.level_one,
        p.foreign_country_filed,
        p.filing_date
    FROM patents_priority p
    JOIN patents_orgs o
    ON p.patent_id = o.patent_id
    WHERE p.filing_date IS NOT NULL
    LIMIT 500;
    """

    df = run_query(query)

    st.dataframe(df)

    # Heatmap
    st.subheader("Heatmap: Country vs Organization")

    pivot = pd.pivot_table(
        df,
        index="foreign_country_filed",
        columns="level_one",
        aggfunc="size",
        fill_value=0
    )

    fig, ax = plt.subplots()
    cax = ax.matshow(pivot)
    fig.colorbar(cax)

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=90)

    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)

    st.pyplot(fig)

# -----------------------------
# Q6: RANKING
# -----------------------------
elif menu == "Ranking (Window Function)":
    st.subheader("🏆 Ranking Agencies by Patent Count")

    query = """
    SELECT 
        fedagency_name,
        COUNT(*) AS total,
        RANK() OVER (ORDER BY COUNT(*) DESC) AS rank
    FROM patents_orgs
    GROUP BY fedagency_name
    ORDER BY total DESC;
    """

    df = run_query(query)

    st.dataframe(df)

    # Scatter plot
    st.subheader("Scatter Plot (Rank vs Total)")
    fig, ax = plt.subplots()
    ax.scatter(df["rank"], df["total"])
    ax.set_xlabel("Rank")
    ax.set_ylabel("Total Patents")
    st.pyplot(fig)