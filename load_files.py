import os
import pandas as pd
from sqlalchemy import create_engine, text
from clean_data import clean_file1, clean_file2
from database import get_engine

RAW_DIR = "data/raw1"
PROCESSED_DIR = "data/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)


# -----------------------------
# STEP 1: READ FILES
# -----------------------------
def process_files():
    file1_path = os.path.join(RAW_DIR, "g_foreign_priority.tsv")
    file2_path = os.path.join(RAW_DIR, "g_gov_interest_org.tsv")

    df1_raw = pd.read_csv(file1_path, sep="\t", engine="python")
    df2_raw = pd.read_csv(file2_path, sep="\t", engine="python")

    print("File1 raw columns:", df1_raw.columns.tolist())
    print("File2 raw columns:", df2_raw.columns.tolist())

    df1_clean = clean_file1(df1_raw)
    df2_clean = clean_file2(df2_raw)

    # Save processed copies (optional but useful)
    df1_clean.to_csv(os.path.join(PROCESSED_DIR, "file1_clean.csv"), index=False)
    df2_clean.to_csv(os.path.join(PROCESSED_DIR, "file2_clean.csv"), index=False)

    return df1_clean, df2_clean


def get_engine():
    return create_engine(
        "postgresql+psycopg2://postgres:bottonse@localhost:5432/patents_db"
    )


def load_to_db(df1, df2):
    engine = get_engine()

    with engine.begin() as conn:

        # =========================
        # FILE 1 INSERT
        # =========================
        for _, row in df1.iterrows():

            # ✅ FIX: convert NaN / NaT → None
            clean_row = {
                k: (None if pd.isna(v) else v)
                for k, v in row.to_dict().items()
            }

            conn.execute(
                text("""
                    INSERT INTO patents_priority (
                        patent_id,
                        priority_claim_sequence,
                        priority_claim_kind,
                        foreign_application_id,
                        filing_date,
                        foreign_country_filed
                    )
                    VALUES (
                        :patent_id,
                        :priority_claim_sequence,
                        :priority_claim_kind,
                        :foreign_application_id,
                        :filing_date,
                        :foreign_country_filed
                    )
                    ON CONFLICT (patent_id)
                    DO UPDATE SET
                        priority_claim_sequence = EXCLUDED.priority_claim_sequence,
                        priority_claim_kind = EXCLUDED.priority_claim_kind,
                        foreign_application_id = EXCLUDED.foreign_application_id,
                        filing_date = EXCLUDED.filing_date,
                        foreign_country_filed = EXCLUDED.foreign_country_filed;
                """),
                clean_row  # ✅ FIX: pass dict directly (NOT keyword arg)
            )

        # =========================
        # FILE 2 INSERT
        # =========================
        for _, row in df2.iterrows():

            # ✅ SAME FIX HERE
            clean_row = {
                k: (None if pd.isna(v) else v)
                for k, v in row.to_dict().items()
            }

            conn.execute(
                text("""
                    INSERT INTO patents_orgs (
                        patent_id,
                        gi_organization_id,
                        fedagency_name,
                        level_one,
                        level_two,
                        level_three
                    )
                    VALUES (
                        :patent_id,
                        :gi_organization_id,
                        :fedagency_name,
                        :level_one,
                        :level_two,
                        :level_three
                    )
                    ON CONFLICT (patent_id)
                    DO UPDATE SET
                        gi_organization_id = EXCLUDED.gi_organization_id,
                        fedagency_name = EXCLUDED.fedagency_name,
                        level_one = EXCLUDED.level_one,
                        level_two = EXCLUDED.level_two,
                        level_three = EXCLUDED.level_three;
                """),
                clean_row  # ✅ FIX
            )

    print("✅ Data loaded successfully into PostgreSQL")