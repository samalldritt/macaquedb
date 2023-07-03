## File is for building database and testing :)

import sqlite3

conn = sqlite3.connect('macaque_db.db')
cursor = conn.cursor()

## Building the database

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Subject (
        subject_id INTEGER PRIMARY KEY,
        site TEXT,
        sessions INTEGER,
        gender TEXT CHECK(gender IN ('MALE', 'FEMALE'))
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Session (
        session_id INTEGER PRIMARY KEY,
        subject_id INTEGER,
        age DOUBLE,
        site TEXT,
        sessions INT,
        FOREIGN KEY (subject_id) REFERENCES Subject (subject_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Image (
        image_id INTEGER PRIMARY KEY,
        session_id INTEGER,
        image_type TEXT,
        image_path TEXT,
        run_number INTEGER,
        FOREIGN KEY (session_id) REFERENCES Session (session_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS JSON (
        json_id INTEGER PRIMARY KEY,
        image_id INTEGER,
        json_path TEXT,
        FOREIGN KEY (image_id) REFERENCES Image (image_id)
    )
''')

conn.commit()
conn.close()