import duckdb
import pandas as pd

# Connect to the same DuckDB database
con = duckdb.connect('inspections.db')

# Load inspections with violations into a DataFrame
inspections_df = con.sql("SELECT inspection_id, violations FROM INSPECTIONS WHERE violations IS NOT NULL").df()

# List to collect rows for VIOLATIONS and INSPECTION_VIOLATIONS tables
violations_data = []
inspection_violations_data = []

# Iterate through inspections and process violations
for _, row in inspections_df.iterrows():
    inspection_id = row['inspection_id']
    violation_str = row['violations']
    violations = violation_str.split('|')

    for violation in violations:
        # Split by period and en-dash to get description and comment
        parts = violation.split('.', 1)
        if len(parts) > 1:
            violation_id = parts[0].strip()
            violation_desc = parts[1].strip()

            # Check if the description contains an optional comment (split by en-dash)
            if ' - ' in violation_desc:
                desc_comment = violation_desc.split(' - ', 1)
                violation_desc = desc_comment[0].strip()
                violation_comment = desc_comment[1].strip() if len(desc_comment) > 1 else None
            else:
                violation_comment = None

            # Escape single quotes
            violation_desc = violation_desc.replace("'", "''")
            if violation_comment:
                violation_comment = violation_comment.replace("'", "''")

            # Collect data for VIOLATIONS
            violations_data.append({'violation_id': violation_id, 'violation_desc': violation_desc})

            # Collect data for INSPECTION_VIOLATIONS
            inspection_violations_data.append({
                'inspection_id': inspection_id,
                'violation_id': violation_id,
                'violation_comment': violation_comment if violation_comment else 'NONE'
            })

# Create DataFrames for violations and inspection_violations
violations_df = pd.DataFrame(violations_data).drop_duplicates(subset=['violation_id'])
inspection_violations_df = pd.DataFrame(inspection_violations_data).drop_duplicates(subset=['inspection_id', 'violation_id', 'violation_comment'])

# Insert into VIOLATIONS table (only unique records)
con.sql("""
    INSERT INTO VIOLATIONS (violation_id, violation_desc)
    SELECT violation_id, violation_desc
    FROM violations_df
    EXCEPT
    SELECT violation_id, violation_desc
    FROM VIOLATIONS
""")

# Generate inspection_violation_id for INSPECTION_VIOLATIONS table
max_id = con.sql("SELECT COALESCE(MAX(inspection_violation_id), 0) FROM INSPECTION_VIOLATIONS").fetchone()[0]
inspection_violations_df['inspection_violation_id'] = range(max_id + 1, max_id + 1 + len(inspection_violations_df))

# Insert into INSPECTION_VIOLATIONS table (only unique records)
con.sql("""
    INSERT INTO INSPECTION_VIOLATIONS (inspection_violation_id, inspection_id, violation_id, violation_comment)
    SELECT inspection_violation_id, inspection_id, violation_id, violation_comment
    FROM inspection_violations_df
""")

# Optionally save to CSV
inspection_violations_df.to_csv('fill-inspection-violations-output.csv', index=False)
