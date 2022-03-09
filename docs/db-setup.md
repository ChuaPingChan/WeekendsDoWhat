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
## Installation (for Windows)
Download the latest version installer. Name database as WeekendsDoWhat.  
Link for reference: https://phoenixnap.com/kb/install-postgresql-windows  
For psql command to work, need to add PATH of PostgreSQL to system settings.


## Create database and user
```
# Start service
brew services start postgresql

# Create database 
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


### Run script
This script creates tables if not exists and copy data from /data to tables.
You can run as many times as possible as the script will clear the database tables before pushing the data.
```
python ./utility/postgresql_setup.py
```