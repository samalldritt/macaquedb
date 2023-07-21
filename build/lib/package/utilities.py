import os

def is_nifti_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension == '.nii.gz' or file_extension == '.gz' or file_extension == '.nii'

def extract_anat_name_from_filename(filename):
    start_index = filename.find('T') + 1
    end_index = filename.find('.')
    if start_index >= 0 and end_index >= 0:
        info = filename[start_index:end_index]
        return info
    else:
        return None