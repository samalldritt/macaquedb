## This file will be for connecting to the database, building, pulling data, etc.

import os
import sqlite3
from Subject import Subject

class Database:

    def __init__(self, db_path):
        self.db_path = db_path
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    '''
    Inserting data through a directory (populating subject tables, session tables, image tables, JSON tables)
    '''
    def input(self, data_dir):
        # Inputting subjects into table
        self.insert_subjects(data_dir)
        
        # Input sessions into table
        
        return
    
    '''
    Loop through all subjects in a 'site-' dir and populate or update into the database
    '''
    def insert_subjects(self, data_dir):
        site_name = os.path.basename(data_dir)
        for subject in os.listdir(data_dir):
            session_count = 0
            subject_dir = os.path.join(data_dir, subject)
            if os.path.isdir(subject_dir) and subject.startswith("sub-"):  # Check if the item is a directory
                subject_id = subject[len('sub-'):]
                for session in os.listdir(subject_dir):
                    session_path = os.path.join(subject_dir, session)
                    if os.path.isdir(session_path) and session.startswith('ses-'):
                        self.insert_session(session_dir=session_path, site_name=site_name, subject_id=subject_id)
                        session_count += 1
                        
                new_sub = Subject(subject_id=subject_id, site=site_name, sessions=session_count)
                self.insert_subject(new_sub)
    
    def insert_session(self, session_dir, site_name, subject_id):
        session_name = os.path.basename(session_dir)
        unique_id = subject_id + '_' + session_name
    
    '''
    Takes in a subject class and inserts it into the database (checking whether it needs to be updated first)
    '''
    def insert_subject(self, subject):
        query_check = "SELECT * FROM Subject WHERE subject_id = ?"
        self.cursor.execute(query_check, (subject.subject_id,))
        existing_subject = self.cursor.fetchone()
        
        attr_names = tuple(subject.__dict__.keys())

        if existing_subject:
            print("Subject already exists in the database:")
            print("Existing row:", existing_subject)

            new_row_values = tuple(getattr(subject, attr) for attr in attr_names)
            print("New row:", new_row_values)
            
            choice = input("Do you want to update the existing subject? (y/n): ")

            if choice.lower() == 'y':
                query_update = f"UPDATE Subject SET {', '.join(f'{name} = ?' for name in attr_names)} WHERE subject_id = ?"
                values = new_row_values + (subject.subject_id,)
                self.cursor.execute(query_update, values)
                self.conn.commit()
                print("Subject updated successfully.")
            else:
                print("Subject not updated.")
        else:
            query_insert = f"INSERT INTO Subject {attr_names} VALUES ({', '.join(['?' for _ in attr_names])})"
            print(query_insert)
            values = tuple(getattr(subject, attr) for attr in attr_names)
            self.cursor.execute(query_insert, values)
            self.conn.commit()
            print("Subject inserted successfully.")
        
    def build(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Subject (
                subject_id TEXT PRIMARY KEY,
                site TEXT,
                sessions INTEGER,
                gender TEXT CHECK(gender IN ('MALE', 'FEMALE'))
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Session (
                session_id TEXT PRIMARY KEY,
                subject_id TEXT,
                age DOUBLE,
                site TEXT,
                FOREIGN KEY (subject_id) REFERENCES Subject (subject_id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Image (
                image_id INTEGER PRIMARY KEY,
                session_id TEXT,
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

    

    

    

