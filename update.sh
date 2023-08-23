#!/bin/bash
# This file will download the CSV file and be called by CRON to update the database .db

demographic_url=https://docs.google.com/spreadsheets/d/e/2PACX-1vQl_ffOrkytiq6wy5eL5CBoi2pAcV7tZoGziXvFPctNmydBSMyovon8TxU9nly7cBHmbLPXFkcbR0H7/pub?gid=599005683&single=true&output=csv

curl -L -o macaquedb.csv "${demographic_url}"

# Now call python script to force update all entires in database
python3 update.py