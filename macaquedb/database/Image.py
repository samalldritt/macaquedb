## Class for images input into the dataframe

class Image:
    
    def __init__(self, image_id, session_id, subject_id, image_type=None, image_subtype=None, image_path=None, run_number=None, site=None):
        self.image_id = image_id
        self.session_id = session_id
        self.subject_id = subject_id
        self.image_type = image_type
        self.image_subtype = image_subtype
        self.image_path = image_path
        self.run_number = run_number
        self.site = site