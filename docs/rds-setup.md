## AWS RDS

### Create database

Standard create -> Amazon Aurora PostgreSQL-Compatible Edition -> PostgreSQL 13.5  
Templates: Dev/Test  
Settings: set username and password to postgres  
DB instance class: Memory optimized -> db.r6g.large (can change but this one cheapest)  
Availability & durability: Don't create an Aurora Replica (save cost)  
Connectivity: Public access -> Yes  
Additional configuration: initial database name -> WeekendsDoWhat (it seems that this cannot be renamed after db creation)  
                          Deletion protection -> disable

### Edit security group od database
Edit inbound rules:   
Add rule -> Type: PostgreSQL; Source: 0.0.0.0/0  
Add rule -> Type: PostgreSQL; Source: ::/0 (Just in case someone use IPv6)

### One way to connect to RDS
1. Install pgadmin (available in both Windows and Mac)
2. Establish a new connection.  
In general tab:  
Name: weekendsdowhat  
In connection tab:  
Connection addr: weekendsdowhat-instance-1.crixlxpvi0ep.ap-southeast-1.rds.amazonaws.com  
Port: 5432  
Username: postgres  
Password: postgres  
3. Change the psycopg2.connect in postgresql_setup.py: 
```
conn = psycopg2.connect(r"host=weekendsdowhat-instance-1.crixlxpvi0ep.ap-southeast-1.rds.amazonaws.com port=5432 dbname=postgres user=postgres password=postgres")
```