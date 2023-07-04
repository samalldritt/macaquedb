import os

def is_nifti_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension == '.nii.gz' or file_extension == '.gz' or file_extension == '.nii'