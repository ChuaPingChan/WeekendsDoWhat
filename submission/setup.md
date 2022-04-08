# Steps for Deployment on AWS
Our SaaS service, WeekendsDoWhat, mainly consists of AWS RDS Aurora PostgreSQL-Compatible Edition database, AWS Elastic  
Beanstalk using Flask for backend and Elastic Beanstalk using React for frontend. The setup order would be database,  
backend and frontend.

## AWS RDS

### Create database on AWS

Standard create -> Amazon Aurora PostgreSQL-Compatible Edition -> PostgreSQL 13.5  
Templates: Dev/Test  
Settings: set username and password to postgres  
DB instance class: Memory optimized -> db.r6g.large (can change but this one cheapest)  
Availability & durability: Don't create an Aurora Replica (save cost)  
Connectivity: Public access -> Yes  
Additional configuration: initial database name -> WeekendsDoWhat (it seems that this cannot be renamed after db creation)  
                          Deletion protection -> enable

### Edit security group of database
Edit inbound rules:   
Add rule -> Type: PostgreSQL; Source: 0.0.0.0/0  
Add rule -> Type: PostgreSQL; Source: ::/0 (Just in case someone use IPv6)

### Create PostgreSQL database on local machine
#### Installation

For Mac:
```
brew install postgresql
brew services start postgresql
```

For Windows:
Download PostgreSQL. Link for reference: https://phoenixnap.com/kb/install-postgresql-windows  
For psql command to work, need to add PATH of PostgreSQL to system settings.

#### Create database and user
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


### Create table and push database to RDS
1. Change the psycopg2.connect in postgresql_setup.py with the endpoint of the previously created AWS RRS: 
```
conn = psycopg2.connect(r"host=weekendsdowhat-instance-1.crixlxpvi0ep.ap-southeast-1.rds.amazonaws.com port=5432 dbname=postgres user=postgres password=postgres")
conn = psycopg2.connect(r"host=[RDS_endpoint] port=5432 dbname=postgres user=postgres password=postgres")
```
2. Run
```
python postgresql_setup.py
```

## AWS Elastic Beanstalk (EBS) for Backend

### Install EBS CLI
(Only if you haven't installed EBS CLI on your local machine)

Follow this [link](https://github.com/aws/aws-elastic-beanstalk-cli-setup) for installation.

### Edit app.py
Change the app.config line, eg:
```
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@mydbcluster.cluster-crixlxpvi0ep.ap-southeast-1.rds.amazonaws.com:5432/WeekendsDoWhat'
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://[rds_username]:[rds_password]@[rds_endpoint]:5432/[rds_db_name]'
```

### Create and launch EBS using command line 
Create environment
```
eb init -p python-3.7 flask-deploy --region ap-southeast-1
eb init -p python-3.7 [env_name] --region ap-southeast-1
```
Create application
```
eb create flask-env
eb create [application_name]
```
If there are any changes, update RDS
```
eb deploy flask-env
eb deploy [application_name]
```

### Edit security group of database
Add one more inbound rule to the created AWS RDS database:  
Add rule -> Type: PostgreSQL; Source: [security group of created EBS backend]

## AWS Elastic Beanstalk (EBS) for Frontend

### Update the URL
In [Constants.js](../Frontend/src/Utils/Constants.js), update the URL (need to include http://)
```
api_endpoint: "http://flask-env3.eba-shnxm3uf.ap-southeast-1.elasticbeanstalk.com"
api_endpoint: "[URL of Flask's EBS]"
```

### Create and launch EBS using command line
Currently, please create in sample application and then deploy the actual code. Direct deployment would result in error.
```
eb init --platform node.js --region ap-southeast-1
```
Create sample application
```
eb create --sample react
eb create --sample [application_name]
```
Deploy the actual code
```
eb deploy
```

### Edit security group of Backend/Flask's Elastic Beanstalk
Add one more inbound rule to the created Backend/Flask's Elastic Beanstalk:  
Add rule -> Type: HTTP; Source: [security group of created Frontend/React's EBS]