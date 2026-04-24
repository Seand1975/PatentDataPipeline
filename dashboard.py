import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

# -----------------------------
# DB CONNECTION
# -----------------------------
DB_URL = "postgresql+psycopg2://postgres:bottonse@localhost:5432/patents_db"
engine = create_engine(DB_URL)

st.set_page_config(page_title="Patent Analytics Dashboard", layout="wide")

st.title("📊 Patent Analytics Dashboard")

# -----------------------------
# QUERY FUNCTIONS
# -----------------------------
def run_query(query):
    return pd.read_sql(query, engine)

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
    st.bar_chart(df.set_index("level_one"))

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
    st.bar_chart(df.set_index("foreign_country_filed"))

# -----------------------------
# Q3: TRENDS OVER TIME
# -----------------------------
elif menu == "Patent Trends Over Time":
    st.subheader("📈 Patent Filings Over Time")

    query = """
    SELECT EXTRACT(YEAR FROM filing_date) AS year, COUNT(*) AS total
    FROM patents_priority
    GROUP BY year
    ORDER BY year;
    """

    df = run_query(query)
    st.dataframe(df)
    st.line_chart(df.set_index("year"))

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
    st.bar_chart(df.set_index("fedagency_name"))

# -----------------------------
# Q5: JOIN VIEW
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
    LIMIT 200;
    """

    df = run_query(query)
    st.dataframe(df)

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