## This file will be for connecting to the database, building, pulling data, etc.

import os
import sqlite3
import re
import uuid
from Subject import Subject
from Session import Session
from Image import Image
from utilities import *

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
        # Inputting data into the table into table
        self.insert_data(data_dir)
        return
    
    '''
    Loop through all subjects in a 'site-' dir and populate or update into the database
    '''
    def insert_data(self, data_dir):
        site_name = os.path.basename(data_dir)
        for subject in os.listdir(data_dir):
            subject_dir = os.path.join(data_dir, subject)
            if os.path.isdir(subject_dir) and subject.startswith("sub-"):  # Check if the item is a directory
                subject_id = subject[len('sub-'):]
                session_count = self.loop_sessions(subject_dir=subject_dir, site_name=site_name, subject_id=subject_id)
                new_sub = Subject(subject_id=subject_id, 
                                  site=site_name, 
                                  sessions=session_count)
                self.insert_subject(new_sub)
    
    '''
    Loop over subjects in dir
    Returns session count for one subject
    '''
    def loop_sessions(self, subject_dir, site_name, subject_id):
        session_count = 0
        for session in os.listdir(subject_dir):
            session_path = os.path.join(subject_dir, session)
            if os.path.isdir(session_path) and session.startswith('ses-'):
                unique_id = subject_id + '_' + session
                new_session = Session(session_id=unique_id,
                                      subject_id=subject_id,
                                      site=site_name)
                self.insert_session(new_session)
                
                ## Also loop all the images within this session
                self.loop_images(session_dir=session_path, subject_id=subject_id, session_id=unique_id)
                session_count += 1
        
        return session_count
    
    '''
    Loop over NIFTI files in a directory and add them all to the database
    '''
    def loop_images(self, session_dir, subject_id, session_id):
        # Walk through every file in session (anat, dwi, fieldmap, func)
        for root, dirs, files in os.walk(session_dir):
            for file in files:
                file_path = os.path.join(root, file)
                abs_file_path = os.path.abspath(file)
                if is_nifti_file(file_path):
                    run_number = re.search(r"run-(\d+)", file)
                    run_number = run_number.group(1)
                    new_image = Image(image_id=str(session_id + '_' + 'run-' + run_number),
                                      session_id=session_id, 
                                      subject_id=subject_id,
                                      image_type=os.path.basename(file_path),
                                      image_path=abs_file_path,
                                      run_number=run_number)
                    self.insert_image(new_image)
            
        pass
    
    '''
    Function to add an image to the database
    '''
    def insert_image(self, image):
        
        ## Check if it is in there already
        query_check = "SELECT * FROM Image WHERE image_id = ?"
        self.cursor.execute(query_check, (image.image_id,))
        existing_image = self.cursor.fetchone()
        
        attr_names = tuple(image.__dict__.keys())
        
        if existing_image:
            print("Image already exists in the database:")
            print("Existing row:", existing_image)
            
            new_row_values = tuple(getattr(image, attr) for attr in attr_names)
            print("New row:", new_row_values)
            
            # Check if all attributes are the same
            all_same = all(existing_image[i] == getattr(image, attr) for i, attr in enumerate(attr_names))
            
            if all_same:
                print("Image is already in database with same attributes, skipping")
                return
            
            choice = input("Do you want to update the existing image? (y/n)")
            
            if choice.lower() == "y":
                query_update = f"UPDATE Image SET {', '.join(f'{name} = ?' for name in attr_names)} WHERE image_id = ?"
                values = new_row_values + (image.image_id,)
                self.cursor.execute(query_update, values)
                self.conn.commit()
                print("Image updated successfully.")
            else:
                print("Image not updated.")
        else:
            query_insert = f"INSERT INTO Image {attr_names} VALUES ({', '.join(['?' for _ in attr_names])})"
            values = tuple(getattr(image, attr) for attr in attr_names)
            self.cursor.execute(query_insert, values)
            self.conn.commit()
            print(f"Image {image.image_id} inserted successfully.")
        
    
    '''
    Adding a specific session to the database
    '''
    def insert_session(self, session):
        
        ## Check if it is in there already
        query_check = "SELECT * FROM Session WHERE session_id = ?"
        self.cursor.execute(query_check, (session.session_id,))
        existing_session = self.cursor.fetchone()
        
        attr_names = tuple(session.__dict__.keys())
        
        if existing_session:
            print("Session already exists in the database:")
            print("Existing row:", existing_session)
            
            new_row_values = tuple(getattr(session, attr) for attr in attr_names)
            print("New row:", new_row_values)
            
            # Check if all attributes are the same
            all_same = all(existing_session[i] == getattr(session, attr) for i, attr in enumerate(attr_names))
            
            if all_same:
                print("Session has no columns to update, skipping")
                return
            
            choice = input("Do you want to update the existing session? (y/n)")
            
            if choice.lower() == "y":
                query_update = f"UPDATE Session SET {', '.join(f'{name} = ?' for name in attr_names)} WHERE session_id = ?"
                values = new_row_values + (session.session_id,)
                self.cursor.execute(query_update, values)
                self.conn.commit()
                print("Session updated successfully.")
            else:
                print("Session not updated.")
        else:
            query_insert = f"INSERT INTO Session {attr_names} VALUES ({', '.join(['?' for _ in attr_names])})"
            values = tuple(getattr(session, attr) for attr in attr_names)
            self.cursor.execute(query_insert, values)
            self.conn.commit()
            print(f"Session {session.session_id} inserted successfully.")
        
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
            
            # Check if all attributes are the same
            all_same = all(existing_subject[i] == getattr(subject, attr) for i, attr in enumerate(attr_names))
            
            if all_same:
                print("Subject has no columns to update, skipping")
                return
            
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
            print(f"Subject {subject.subject_id} inserted successfully.")
        
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
                image_id TEXT PRIMARY KEY,
                session_id TEXT,
                subject_id TEXT,
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

    

    

    

