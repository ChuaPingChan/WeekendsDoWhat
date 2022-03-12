# PostgreSQL

Guide: 
- https://www.prisma.io/dataguide/postgresql
- https://www.sqlshack.com/setting-up-a-postgresql-database-on-mac/

UI: https://www.pgadmin.org/

## Installation

For Mac:
```
brew install postgresql
brew services start postgresql
```

For Windows:
Download PostgreSQL. Link for reference: https://phoenixnap.com/kb/install-postgresql-windows  
For psql command to work, need to add PATH of PostgreSQL to system settings.


## Create database and user
```
# Start service
brew services start postgresql

# Create database with the name "WeekendsDoWhat"
$ createdb WeekendsDoWhat

# Login to database
$ psql WeekendsDoWhat

[Optional]
# Create user `postgres`
CREATE ROLE postgres WITH LOGIN PASSWORD 'password';

# Login using new user's credentials
/q
psql WeekendsDoWhat -U postgres
```

## Using Python to create table and push data
1. Change or add the database connection string in [utility/postgresql_setup.py](utility/postgresql_setup.py) and [app.py](app.py) appropriately.
1. Run
    ```
    python ./utility/postgresql_setup.py
    ```
    This script creates tables if not exists and copy data from /data to tables.
You can run as many times as possible as the script will clear the database tables before pushing the data.
