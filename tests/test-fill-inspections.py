import duckdb

# Connect to the same DuckDB database
con = duckdb.connect('inspections.db')

# Run a query to verify data in the INSPECTIONS table
result = con.execute("SELECT * FROM INSPECTIONS WHERE VIOLATIONS IS NOT NULL LIMIT 10").fetchall()

# Print the results to verify
for row in result:
    print(row)

# Optionally, you can check how many rows are in the table
row_count = con.execute("SELECT COUNT(*) FROM INSPECTIONS").fetchone()[0]
print(f"Total number of rows in INSPECTIONS: {row_count}")
