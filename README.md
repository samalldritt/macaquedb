# Python SQLite interface for PRIME-DE data

Simplified way to interact and add / pull data from SQL tables designed to hold our neuroimaging data.

## Getting started

Installing:
```
pip install macaquedb
```

Importing and creating link to database:
```
python3
>>> import macaquedb
>>> interface = macaquedb.Database('/path/to/database')
```
If the interface is not built yet, declaring the path will set the install directory. Then you can use:
```
>>> interface.build()
```
This will build the tables and the .db file. This file stores the data. If we move the .db file, you need to point the interface to the new location with:
```
interface.changePath('/new/path/to/database')
```
## Tables and adding data
In the current version, we have 4 tables that are connected:
### Subjects:
| Column Name | Data Type         |
|-------------|------------------|
| subject_id  | TEXT (Primary Key)|
| site        | TEXT             |
| sessions    | INTEGER          |
| gender      | TEXT             |
### Sessions:
| Column Name | Data Type         | References         |
|-------------|------------------|--------------------|
| session_id  | TEXT (Primary Key)|                    |
| subject_id  | TEXT             | Subject(subject_id)|
| age         | DOUBLE           |                    |
| site        | TEXT             |                    |
| image_count | INT              |                    |
### Images:
| Column Name   | Data Type         | References         |
|---------------|------------------|--------------------|
| image_id      | TEXT (Primary Key)|                    |
| session_id    | TEXT             | Session(session_id)|
| subject_id    | TEXT             | Subject(subject_id)|
| image_type    | TEXT             |                    |
| image_subtype | TEXT             |                    |
| image_path    | TEXT             |                    |
| mask_path     | TEXT             |                    |
| run_number    | INTEGER          |                    |
| site          | TEXT             |                    |
### JSONS
| Column Name | Data Type        | References      |
|-------------|------------------|-----------------|
| json_id     | INTEGER (Primary Key)|               |
| image_id    | INTEGER          | Image(image_id) |
| json_path   | TEXT             |                 |

To add data:
```
interface.input_site('/path/to/site-site')
interface.input_demographics(csv_path='/path/to/csv.csv', subject_column='SubColName', session_column='SesColName', age_column='AgeColName', sex_column='SexColName')
```
You can also pick and choose any column you want to extract and return a pandas dataframe or just export straight to a CSV
Extracting data:
```
colNamesToExtract = ("subject_id", "session_id", "age", "sex", "image_path", "run_number")
dataframe = interface.make_csv(colNamesToExtract, '/path/to/output.csv')
```
