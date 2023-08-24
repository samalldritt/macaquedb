import logging
from macaquedb.Database import Database
from datetime import datetime
import sys
import os

class TimestampFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{timestamp} - {super().format(record)}"

current_datetime = datetime.now()
timestamp = current_datetime.strftime("%d-%m-%Y_%H-%M-%S")
log_file_path = f"/home/projects/PRIME-DE/database/macaquedb/logs/{timestamp}_log.txt"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d_%H-%M-%S')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
formatter = TimestampFormatter('%(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

# Redirect stdout and stderr to the log file
sys.stdout = file_handler.stream
sys.stderr = file_handler.stream

data_dir_1 = '/home/projects/PRIME-DE/database/PRIME-DE1_BIDS'
data_dir_2 = '/home/projects/PRIME-DE/database/PRIME-DE2_BIDS'

try:
    interface = Database('/home/projects/PRIME-DE/database/macaquedb/macaquedb.db')

    for dirs in os.listdir(data_dir_1):
        input_path = os.path.join(data_dir_1, dirs)
        interface.input_site(input_path, force=True)

    for dirs in os.listdir(data_dir_2):
        input_path = os.path.join(data_dir_2, dirs)
        interface.input_site(input_path, force=True)

    interface.insert_demographics("/home/projects/PRIME-DE/database/macaquedb/macaquedb.csv", subject_column="BIDS_subID", session_column="BIDS_session", age_column="Age(Years)", sex_column="Sex")

    interface.close()

    logger.info("Database update successful")
except Exception as e:
    logger.exception("An error occurred during the database update: %s", str(e))
