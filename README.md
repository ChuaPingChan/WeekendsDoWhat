### Environment Setup
1. Install Python 3.9
    - On Windows, check the option to enable Python to be added to the PATH environment variable during installation. Otherwise, [add the path of Python to the PATH environment variable manually](https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/).
1. Create an python environment using Conda [Optional]

    ```
    conda create --name cloud python=3.9.7
    conda activate cloud
    ```

1. Install packages
    ```
    pip install flask psycopg2-binary psycopg2 flask-sqlalchemy
    ```
1. Start a shell in this project's root directory to run the backend
    
    1. Set the following environment variables in your shell:
    
       ```
       # Windows CMD
       set ENV=dev
       set postgres_pwd=<YourPostgresDbPassword>

       # Mac
       export ENV=dev
       export postgres_pwd=<YourPostgresDbPassword>
       ```
    1. Create a PostgreSQL database and populate it following the steps in [docs/db-setup.md](docs/db-setup.md).
        
    
    1. Run the Flask backend
        ```
        python ./Backend/server.py
        ```
1. Start another shell in this project's root directory to run the frontend
    1. Change the current working directory to ./Frontend
    1. Follow the steps in [docs/frontend.md](docs/frontend.md)

