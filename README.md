### Environment Setup
(If Windows, need to add PATH of pipenv to system settings.
https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/  
Pipfile using Python 3.9)

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
    python ./Backend/app.py
    ```
1. Run the frontend following [docs/frontend.md](docs/frontend.md).

### Package Management

To add new packages to the `pipenv` environment
```
pipenv install <package-name>
```
