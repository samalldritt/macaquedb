## This file will be for connecting to the database, building, pulling data, etc.

import os
import sqlite3

class Database:

    def __init__(self, db_path):
        self.db_path = db_path
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
    def populate(self, inputDir):
        self.inputData = inputDir
        directory_names = [item for item in os.listdir(self.inputData) if os.path.isdir(os.path.join(self.inputData, item))] # Get subject paths
        
        for subject_path in directory_names:
            self.populateSubjectTable(subject_path, self.inputData)
            
            
        self.conn.close()
            
    def populateSubjectTable(self, filename, root_path):
        '''
        ## Data should be in BIDS format, need to grab and populate in this order:
         - Subject ID (Int)
         - Site (String)
         - Session Count (Int)
         - Gender (Male/Female, String)
        '''
        subject_id = filename[len('sub-'):]
        site = os.path.basename(root_path)
        
        ## Count number of sessions
        session_count = 0
        sessions = os.listdir(os.path.join(root_path, filename))
        for session in sessions:
            session_path = os.path.join(root_path, filename, session)
            if os.path.isdir(session_path) and session.startswith('ses-'):
                session_count += 1
                
        column_names = ['subject_id', 'site', 'sessions']
        values = [subject_id, site, session_count]
        command = f"INSERT INTO 'Subject' ({', '.join(column_names)}) VALUES (?, ?, ?)"

        ## Add to database
        self.cursor.execute(command, values)
        
        self.conn.commit()
        
    def removeSite(self, )    
        
    
    def build(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Subject (
                subject_id INTEGER PRIMARY KEY,
                site TEXT,
                sessions INTEGER,
                gender TEXT CHECK(gender IN ('MALE', 'FEMALE'))
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Session (
                session_id INTEGER PRIMARY KEY,
                subject_id INTEGER,
                age DOUBLE,
                site TEXT,
                sessions INT,
                FOREIGN KEY (subject_id) REFERENCES Subject (subject_id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Image (
                image_id INTEGER PRIMARY KEY,
                session_id INTEGER,
                image_type TEXT,
                image_path TEXT,
                run_number INTEGER,
                FOREIGN KEY (session_id) REFERENCES Session (session_id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS JSON (
                json_id INTEGER PRIMARY KEY,
                image_id INTEGER,
                json_path TEXT,
                FOREIGN KEY (image_id) REFERENCES Image (image_id)
            )
        ''')

        self.conn.commit()
        return
    
    def close(self):
        self.conn.close()

    

    

    

