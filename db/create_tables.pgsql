CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,                
    full_name TEXT NOT NULL,              
    age INT NOT NULL,                     
    workplace TEXT,                       
    contacts TEXT NOT NULL,               
    description TEXT,
    file_path TEXT NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT * FROM submissions;