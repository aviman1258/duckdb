import duckdb

# Connect to the same DuckDB database
con = duckdb.connect('inspections.db')

row_count = con.execute("SELECT COUNT(*) FROM VIOLATIONS").fetchone()[0]
print(f"Total number of rows in VIOLATIONS: {row_count}")

# Optionally, you can check how many rows are in the table
row_count = con.execute("SELECT COUNT(*) FROM INSPECTION_VIOLATIONS").fetchone()[0]
print(f"Total number of rows in INSPECTION_VIOLATIONS: {row_count}")

#18717 inspection_violation
#59 violation
