import pandas as pd
from sqlalchemy import create_engine

# ---------- CONFIG ----------
DB_USER = "postgres"
DB_PASS = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "dsf_2025_poc"

DATA_PATH = "data/cleaned"
# ----------------------------

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def load_csv(table_name, filename, dtype_map=None):
    path = f"{DATA_PATH}/{filename}"
    print(f"Loading {filename} → {table_name}...")
    df = pd.read_csv(path)
    df.to_sql(table_name, engine, if_exists="replace", index=False, dtype=dtype_map)
    print(f"{table_name} loaded")

# Load each table
load_csv("courses", "courses.csv")
load_csv("sections", "sections.csv")
load_csv("instructors", "instructors.csv")
load_csv("meeting_times", "meeting_times.csv")

print("All tables loaded into PostgreSQL.")