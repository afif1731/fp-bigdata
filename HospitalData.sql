-- Clean the database
DROP TABLE IF EXISTS Patient_Readmissions;

-- Create the Schema
CREATE TABLE IF NOT EXISTS Patient_Readmissions(
            age INT NOT NULL,
            gender VARCHAR(10) NOT NULL,
            primary_diagnosis VARCHAR(125) NOT NULL,
            num_procedures INT NOT NULL,
            days_in_hospital INT NOT NULL,
            comorbidity_score INT NOT NULL,
            discharge_to VARCHAR(125) NOT NULL,
            readmitted INT NOT NULL
);