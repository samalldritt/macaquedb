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

