
import sqlite3
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
database_path = project_dir / "data" / "retail_sales.db"

#Creating database connection function & connect to SQLite database
def get_connection():
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    return connection

#Creating the sales table
def create_sales_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            transaction_id TEXT PRIMARY KEY,
            transaction_date TEXT,
            product TEXT,
            quantity INTEGER,
            unit_price REAL,
            city TEXT,
            total_sales REAL
        )
    """)
    connection.commit()


#Creating Database
def initialize_database():
    connection = get_connection()
    create_sales_table(connection)
    create_rejected_sales_table(connection)
    connection.close()



def load_dataframe(df, table_name):
    allowed_tables = {"sales", "rejected_sales"}

    if table_name not in allowed_tables:
        raise ValueError(f"Unsupported table name: {table_name}")

    connection = get_connection()

    try:
        # Remove the previous run's records
        connection.execute(f"DELETE FROM {table_name}")

        # Insert the current run's records
        df.to_sql(
            table_name,
            connection,
            if_exists="append",
            index=False
        )

        connection.commit()

    finally:
        connection.close()




#Adding the rejected records table
def create_rejected_sales_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS rejected_sales (
            transaction_id TEXT,
            transaction_date TEXT,
            product TEXT,
            quantity REAL,
            unit_price REAL,
            city TEXT,
            rejection_reason TEXT
        )
    """)
    connection.commit()

