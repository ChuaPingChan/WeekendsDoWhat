### Environment Setup
1. Install Python 3.9
    - On Windows, check the option to enable Python to be added to the PATH environment variable during installation. Otherwise, [add the path of Python to the PATH environment variable manually](https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/).
1. Activate virtual environment
    ```
    pipenv shell
    ```
1. Create a PostgreSQL database and populate it following the steps in [docs/db-setup.md](docs/db-setup.md).
1. Set the following environment variables in your shell:
   ```
   ENV=dev
   postgres_pwd=<YourPostgresDbPassword>
   ```
    (If flask not installed, run 'pip install flask' and 'pip install flask_sqlalchemy)
1. Run the Flask backend
    ```
    python ./Backend/server.py
    ```
1. Run the frontend following [docs/frontend.md](docs/frontend.md).

### Package Management

To add new packages to the `pipenv` environment
```
pipenv install <package-name>
```
