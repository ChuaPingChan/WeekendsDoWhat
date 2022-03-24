## DB

Aurora PostgreSQL
 - Multi-AZ, ap-southeast-1a (Writer), ap-southeast-1b (Reader)
 - security group
    - allow Flask security group on port 5432

FrontEnd 
 - Elastic beanstalk
    - security group
    - load balancer
    - auto scaling group
    - EC2 instances
    - Cloudwatch alarms

Flask
 - Elastic beanstalk
    - security group
        - allow FrontEnd security group on port 80
    - load balancer
    - auto scaling group
    - EC2 instances
    - Cloudwatch alarms