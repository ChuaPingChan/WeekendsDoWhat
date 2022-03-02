# PostgreSQL

Guide: 
- https://www.prisma.io/dataguide/postgresql
- https://www.sqlshack.com/setting-up-a-postgresql-database-on-mac/

UI: https://www.pgadmin.org/

## Installation (for Mac)
```
brew install postgresql
brew services start postgresql
```

## Create database and user
```
# Start service
brew services start postgresql

# Create database 
$ createdb postgres

# Login to database
$ psql postgres

[Optional]
# Create user `postgres`
CREATE ROLE postgres WITH LOGIN PASSWORD 'password';

# Login using new user's credentials
/q
psql postgres -U postgres
```

## Using Python to create table and push data 

### Install psycopg2 library via pip
```
pip install psycopg2
```

### Run script
```
python postgresql_setup.py
```