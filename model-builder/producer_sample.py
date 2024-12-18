import os
import pandas as pd
from sqlalchemy import create_engine

# Fungsi untuk mendapatkan environment variable
def get_env_var(var_name):
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable '{var_name}' is not set!")
    return value

# Fetch environment variables
POSTGRES_USER = get_env_var("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_var("POSTGRES_PASSWORD")
POSTGRES_ENDPOINT = get_env_var("POSTGRES_ENDPOINT")
POSTGRES_DB = get_env_var("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")  # Default port 5432

# File path ke data sumber
data_source_path = "../dataset/data/patient_readmissions.csv"  # Ganti dengan path file Anda

# PostgreSQL connection string
postgres_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_ENDPOINT}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create database connection
engine = create_engine(postgres_url)

# Load data ke PostgreSQL
def load_data_to_postgres(file_path, table_name, engine):
    print(f"Loading data from {file_path} to table '{table_name}'...")
    try:
        # Baca data menggunakan Pandas
        df = pd.read_csv(file_path)
        
        # Menulis data ke PostgreSQL
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        
        print(f"Data successfully loaded into table '{table_name}'.")
    except Exception as e:
        print(f"Error loading data: {e}")

if __name__ == "__main__":
    # Nama tabel tujuan di PostgreSQL
    table_name = "patient_readmissions"

    # Jalankan proses load data
    load_data_to_postgres(data_source_path, table_name, engine)
