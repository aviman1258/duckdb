import duckdb

# Connect to (or create) the database
con = duckdb.connect('inspections.db')

# Read the schema.sql file and execute the statements
with open('schema.sql', 'r') as schema_file:
    schema_sql = schema_file.read()

# Execute the schema to create the tables
con.execute(schema_sql)

# Load data directly from the CSV file into the INSPECTIONS table
con.execute("""
    COPY INSPECTIONS FROM 'restaurants-subset.csv' (AUTO_DETECT TRUE);
""")
