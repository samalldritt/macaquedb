import sys
import os
import logging
from macaquedb.Database import Database
from datetime import datetime
from io import StringIO

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d_%H-%M-%S')
logger = logging.getLogger(__name__)

data_dir_1 = '/home/projects/PRIME-DE/database/PRIME-DE1_BIDS'
data_dir_2 = '/home/projects/PRIME-DE/database/PRIME-DE2_BIDS'

try:
    interface = Database('macaquedb.db')

    # Capture standard output and standard error
    stdout_backup = sys.stdout
    stderr_backup = sys.stderr
    sys.stdout = sys.stderr = output_buffer = StringIO()

    # Walk through and input the site directories
    for dirs in os.listdir(data_dir_1):
        input_path = os.path.join(data_dir_1, dirs)
        interface.input_site(input_path, force=True)

    for dirs in os.listdir(data_dir_2):
        input_path = os.path.join(data_dir_2, dirs)
        interface.input_site(input_path, force=True)

    interface.insert_demographics("macaquedb.csv", subject_column="BIDS_subID", session_column="BIDS_session", age_column="Age(Years)", sex_column="Sex")

    interface.close()

    # Restore standard output and standard error
    sys.stdout = stdout_backup
    sys.stderr = stderr_backup

    # Log captured output
    output_text = output_buffer.getvalue()
    if output_text.strip():  # Check if there's any output to log
        logger.info("Captured output:\n%s", output_text)
    
    logger.info("Database update successful")
except Exception as e:
    logger.exception("An error occurred during the database update: %s", str(e))