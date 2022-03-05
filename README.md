### Environment Setup

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
1. Run the Flask backend
    ```
    python app.py
    ```
1. Run the frontend following [docs/frontend.md](docs/frontend.md).

### Package Management

To add new packages to the `pipenv` environment
```
pipenv install <package-name>
```
