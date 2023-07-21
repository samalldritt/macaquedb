## Populate a session table

class Session:
    
    def __init__(self, session_id=None, subject_id=None, age=None, site=None, image_count=None):
        self.session_id = session_id
        self.subject_id = subject_id
        self.age = age
        self.site = site
        self.image_count = image_count