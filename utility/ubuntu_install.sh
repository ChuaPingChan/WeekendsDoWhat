#!/bin/bash

sudo apt-get update && sudo apt-get -y install git 
sudo apt update && sudo apt -y install curl python3-pip postgresql postgresql-contrib

# Setup frontend
## Install nodejs v16.14.0
curl -sL https://deb.nodesource.com/setup_16.x -o ~/nodesource_setup.sh
sudo bash ~/nodesource_setup.sh
sudo apt -y install nodejs
node -v # verify version

cd Frontend && npm install && cd ..

# Setup App
pip install -r requirements.txt
sudo apt update && sudo apt -y install python3-flask

# Setup Database
sudo systemctl start postgresql
sudo su - postgres -c "createdb WeekendsDoWhat"
## comment out if need to setup role and credentials
# sudo su - postgres -c "psql WeekendsDoWhat"
# CREATE ROLE postgres WITH LOGIN PASSWORD 'password';
# ALTER ROLE postgres WITH PASSWORD 'password';
# \q

export FLASK_ENV="development"
export postgres_pwd="password"
python3 ./utility/postgresql_setup.py