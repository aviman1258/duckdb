DROP TABLE IF EXISTS INSPECTION_VIOLATIONS;
DROP TABLE IF EXISTS VIOLATIONS;
DROP TABLE IF EXISTS INSPECTIONS;

CREATE TABLE INSPECTIONS (
    inspection_id INTEGER PRIMARY KEY,
    dba_name VARCHAR,                
    aka_name VARCHAR,                
    license_number FLOAT,            
    facility_type VARCHAR,            
    risk VARCHAR,                    
    address VARCHAR,                  
    city VARCHAR,                    
    state VARCHAR,                    
    zip FLOAT,                        
    inspection_date DATE,            
    inspection_type VARCHAR,          
    results VARCHAR,                  
    violations TEXT,                  
    latitude DOUBLE, 
    longitude DOUBLE,                
    location VARCHAR                  
);

CREATE TABLE VIOLATIONS (
    violation_id INTEGER PRIMARY KEY,
    violation_desc TEXT
);

CREATE TABLE INSPECTION_VIOLATIONS (
    inspection_violation_id INTEGER PRIMARY KEY,
    inspection_id INTEGER,
    violation_id INTEGER,
    violation_comment TEXT,
    FOREIGN KEY (inspection_id) REFERENCES INSPECTIONS(inspection_id),
    FOREIGN KEY (violation_id) REFERENCES VIOLATIONS(violation_id)
);