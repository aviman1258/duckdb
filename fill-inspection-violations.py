import duckdb

# Connect to the same DuckDB database
con = duckdb.connect('inspections.db')



inspections = con.sql("SELECT inspection_id, violations FROM INSPECTIONS WHERE violations IS NOT NULL").fetchall()

for inspection_id, violation_str in inspections:
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

            # Escape single quotes in violation_desc and violation_comment
            violation_desc = violation_desc.replace("'", "''")

            if violation_comment:
                violation_comment = violation_comment.replace("'", "''")

            # Check if this violation already exists in the VIOLATIONS table
            existing_violation = con.sql(f"""
                SELECT 1 FROM VIOLATIONS
                WHERE violation_id = {violation_id}
            """).fetchone()

            if not existing_violation:
                # Insert new violation (if it doesn't exist)
                con.sql(f"""
                    INSERT INTO VIOLATIONS (violation_id, violation_desc)
                    VALUES ({violation_id},'{violation_desc}')
                """)   

            # Check if a row with the same inspection_id, violation_id, and violation_comment already exists
            existing_inspection_violation = con.sql(f"""
                SELECT 1 FROM INSPECTION_VIOLATIONS
                WHERE inspection_id = {inspection_id}
                AND violation_id = {violation_id}
                AND violation_comment = '{violation_comment}'
            """).fetchone()

            if not existing_inspection_violation:             

                # Generate new inspection_violation_id by finding the max value and incrementing it
                max_id = con.sql("SELECT COALESCE(MAX(inspection_violation_id), 0) FROM INSPECTION_VIOLATIONS").fetchone()[0]
                new_inspection_violation_id = max_id + 1

                # Insert into INSPECTION_VIOLATIONS table
                con.sql(f"""
                    INSERT INTO INSPECTION_VIOLATIONS (inspection_violation_id, inspection_id, violation_id, violation_comment)
                    VALUES ({new_inspection_violation_id}, {inspection_id}, {violation_id}, '{violation_comment}')
                """)