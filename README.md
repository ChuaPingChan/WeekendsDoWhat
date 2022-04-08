### For Ubuntu server setup

1. (First time only) Setup of the frontend, backend server and postgres
    ```
    bash utility/ubuntu_install.sh
    ```
    If you see this error below
    ```
    Traceback (most recent call last):
    File "./utility/postgresql_setup.py", line 12, in <module>
        conn = psycopg2.connect(f"host=localhost port=5432 dbname=WeekendsDoWhat user=postgres password={os.environ['postgres_pwd']}")
    File "/home/weekends/.local/lib/python3.8/site-packages/psycopg2/__init__.py", line 122, in connect
        conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
    psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL:  password authentication failed for user "postgres"
    connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL:  password authentication failed for user "postgres"
    ```
    you need to update the `postgres` user password by running
    ```
    sudo su - postgres -c "psql WeekendsDoWhat"
    ALTER ROLE postgres WITH PASSWORD 'password';
    \q
    ```
    and retry the command `bash utility/ubuntu_install.sh`
1. In subsequent sessions, just set the environment variables
    | Environment Variable Name | Value                 | Remarks |
    | ------------------------- | --------------------- | -------- |
    | FLASK_APP                 | "application"         ||
    | FLASK_ENV                 | "development"           | Set this only if you are running the server locally |
    | postgres_pwd              | PostgreSQL database password  | PostgreSQL password on our Ubuntu VM is "password" |
    | ENV                       | "aws"     | Set this only on AWS (e.g., EC2, Elastic Beanstalk) |
1. To run the server
    ```
    flask run --host=0.0.0.0 --port=5050
    ```
    To run the frontend
    ```
    cd Frontend && npm start
    ```

### Setup and Run the Server
1. Install Python 3.9.7
    - On Windows, check the option to enable Python to be added to the PATH environment variable during installation. Otherwise, [add the path of Python to the PATH environment variable manually](https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/).
1. Start a shell and change the working directory to this project's root directory
1. Create and activate a python environment (Optional)
    1. Using Conda
        ```
        conda create --name cloud python=3.9.7
        conda activate cloud
        ```
    1. Using venv

        (First time only) If on Ubuntu, install python3-venv
        ```
        sudo apt update && sudo apt -y install python3-venv
        ```
        (First time only) Create the venv folder
        ```
        python -m venv venv
        ```
        Activate the virtual environment
        ```
        # Mac/Ubuntu
        source venv/bin/activate

        # Windows CMD
        venv\Scripts\activate
        ```
1. Install packages
    ```
    pip install -r requirements.txt
    ```
1. Set the following environment variables in your shell:
    | Environment Variable Name | Value                 | Remarks |
    | ------------------------- | --------------------- | -------- |
    | FLASK_APP                 | "application"         ||
    | FLASK_ENV                 | "development"           | Set this only if you are running the server locally |
    | postgres_pwd              | PostgreSQL database password  | PostgreSQL password on our Ubuntu VM is "password" |
    | ENV                       | "aws"     | Set this only on AWS (e.g., EC2, Elastic Beanstalk) |
1. If this is the first time you are setting up the database, populate the newly create database following the steps in [docs/db-setup.md](docs/db-setup.md).
1. Run the Flask backend
    ```
    flask run --host=0.0.0.0 --port=<port_num>
    ```

### Setup and Run the Frontend server
1. Start a shell and change the working directory to "./Frontend"
1. Follow the steps in [docs/frontend.md](docs/frontend.md)
