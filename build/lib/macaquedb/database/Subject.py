# File for Subject class for Database

class Subject:

    # Columns of table for input parameters
    def __init__(self, subject_id=None, site=None, sessions=None, sex=None):
        self.subject_id = subject_id
        self.site = site
        self.sessions = sessions
        self.sex = sex
