import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace('"', '', regex=False)
        .str.replace(" ", "_")
    )
    return df


# ---------------- FILE 1: PRIORITY DATA ----------------
def clean_file1(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = normalize_columns(df)

    expected_cols = [
        "patent_id",
        "priority_claim_sequence",
        "priority_claim_kind",
        "foreign_application_id",
        "filing_date",
        "foreign_country_filed"
    ]

    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"File1 missing columns: {missing}\nGot: {df.columns.tolist()}")

    df = df[expected_cols]

    df["filing_date"] = pd.to_datetime(df["filing_date"], errors="coerce")

    df = df.drop_duplicates()
    df = df.dropna(subset=["patent_id"])

    return df.head(300)


# ---------------- FILE 2: ORGANIZATION DATA ----------------
def clean_file2(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = normalize_columns(df)

    expected_cols = [
        "patent_id",
        "gi_organization_id",
        "fedagency_name",
        "level_one",
        "level_two",
        "level_three"
    ]

    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"File2 missing columns: {missing}\nGot: {df.columns.tolist()}")

    df = df[expected_cols]

    df = df.drop_duplicates()
    df = df.dropna(subset=["patent_id"])

    return df.head(300)