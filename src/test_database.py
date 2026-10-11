
from database import get_connection

connection = get_connection()

try:
    # Check the number of records in each table
    for table_name in ("sales", "rejected_sales"):
        count = connection.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

        print(f"{table_name}: {count} records")

    # Check total sales in the database
    result = connection.execute("""
        SELECT SUM(total_sales)
        FROM sales
    """).fetchone()[0]

    print(f"Total sales: ₹{result:,.2f}")

    # View sales grouped by city
    rows = connection.execute("""
        SELECT city, SUM(total_sales) AS total_sales
        FROM sales
        GROUP BY city
        ORDER BY city
    """).fetchall()

    print("\nSales by city:")
    for row in rows:
        print(row)

finally:
    connection.close()
