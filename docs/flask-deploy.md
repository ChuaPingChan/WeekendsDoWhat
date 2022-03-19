## EBS Flask
Only tested on Ubuntu

### Create RDS database
Follow the steps in [rds-setup.md](rds-setup.md)

###Install EBS CLI
(Only for first time. It's better to install this on your local machine rather than the shared one because u also need AWS credentials to access the EBS) 

Follow this [link](https://github.com/aws/aws-elastic-beanstalk-cli-setup) for installation.

### Edit app.py 
Important: For some reasons, cannot use the keyword app on EBS. Please replace all app with application (including filename and code).  
Change the app.config line, eg:  
```
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@mydbcluster.cluster-crixlxpvi0ep.ap-southeast-1.rds.amazonaws.com:5432/WeekendsDoWhat'
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://[rds_username]:[rds_password]@[rds_endpoint]:5432/[rds_db_name]'
```

###Create and launch EBS using command line
Currently, please only place application.py and requirements.txt in the folder and launch the terminal  
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

###Edit security group of database
Add one more inbound rule to the created RDS database:  
Add rule -> Type: PostgreSQL; Source: [security group of created EBS]

###Debug
After the creation of EBS is completed, go to the application -> Logs -> Request Logs -> Full Logs ->  
Download zip file -> eb-engine.log (most of the useful info is in this file)