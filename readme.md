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
## To revert migrations:

```
alembic downgrade %revision_num%
OR
alembic downgrade base - To revert all migrations
```
## To execute calls:

```
Create a user in /register
Register a user in /login
Insert Token in to request as a Header in form :
Authorization : Bearer Your_JWT_Token
```

## To use swagger:
```
go to /docs endpoint
register a user
login
hit Authorize and pass bearer token
```
test
