# Patent Data Pipeline

This project builds a data pipeline that cleans tsv files from uspto,
transforms it using pandas, and loads it into a PostgreSQL database.

## Features

- Data normalization into 2 tables:
  - patents_org
  - patents_priority
 
- Modular ETL design

## Setup

1. Clone repo
2. Install dependencies:
   pip install -r requirements.txt

3. Setup PostgreSQL:
   CREATE DATABASE patents_db;

4. Run schema do this in project directory:
   psql -d patents_db -f schema.sql

5. Set environment variable:
   export DB_URI=postgresql://user:password@localhost:5432/patents_db

6. Run pipeline:
   python main.py

7. Run Dashboard
   pip install streamlit sqlalchemy psycopg2 pandas
   python -m streamlit run dashboard.py
