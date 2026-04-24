from sqlalchemy import text
from database import get_engine


def run_queries():
    engine = get_engine()

    with engine.connect() as conn:
        with open("queries.sql", "r") as f:
            raw_sql = f.read()

        queries = [q.strip() for q in raw_sql.split(";") if q.strip()]

        for i, query in enumerate(queries, start=1):
            print(f"\n--- Running Query Q{i} ---\n")

            try:
                result = conn.execute(text(query))

                # Print column names
                if result.returns_rows:
                    columns = result.keys()
                    print(" | ".join(columns))
                    print("-" * 50)

                    for row in result.fetchall():
                        print(" | ".join(str(x) for x in row))
                else:
                    print("Query executed successfully (no rows returned).")

            except Exception as e:
                print(f"Error in Query Q{i}: {e}")