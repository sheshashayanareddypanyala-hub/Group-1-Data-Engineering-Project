print("Script started...")
import pandas as pd
from sqlalchemy import create_engine

# Load your CSV file
df = pd.read_csv("meetings_postgres_ready_final_v5.csv")

print("CSV Loaded. Rows:", len(df))

#Create connection engine
engine = create_engine(
    "postgresql+psycopg2://postgres:Postgres123!@meetings-postgres-db.cfgm80wau5t9.eu-north-1.rds.amazonaws.com:5432/postgres"
)

#Upload to PostgreSQL
df.to_sql(
    name="meetings_postgres_ready_final_v5",   # table name in RDS
    con=engine,
    if_exists="replace",   # replace if exists
    index=False
)

print("Upload successful!")
