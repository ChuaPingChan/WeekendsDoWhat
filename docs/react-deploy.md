## EBS React
Only tested on Ubuntu

### Update the URL
In [Constants.js](Frontend/src/Utils/Constants.js), update the URL (need to include http://)
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

### Edit security group of Flask's Elastic Beanstalk
Add one more inbound rule to the created Flask's Elastic Beanstalk:  
Add rule -> Type: HTTP; Source: [security group of created React's EBS]
