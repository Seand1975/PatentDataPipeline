# Patent Data Pipeline

This project builds a data pipeline that extracts patent data from the USPTO API,
transforms it using pandas, and loads it into a PostgreSQL database.

## Features
- Multi-page API extraction
- Data normalization into 4 tables:
  - patents
  - inventors
  - companies
  - relationships
- Modular ETL design

## Setup

1. Clone repo
2. Install dependencies:
   pip install -r requirements.txt

3. Setup PostgreSQL:
   CREATE DATABASE patents_db;

4. Run schema:
   psql -d patents_db -f models/schema.sql

5. Set environment variable:
   export DB_URI=postgresql://user:password@localhost:5432/patents_db

6. Run pipeline:
   python main.py