## Overview:
```
A Simple FastApi blog API
```

## Prerequisites:
 PostgresSQL16, Python3, pip3 
## To run the project:

```
pip install -r requirements.txt
Create .env file with DATABASE_URL variable as a connection to your db
python3 main.py
```

## To run migrations:

```
alembic revision -m "Name of the migration"
Navigate to alembic/versions/newfile
Configure update and downgrade functions
alembic upgrade head
```
