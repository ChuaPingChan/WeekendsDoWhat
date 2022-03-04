### Environment Setup

1. Activate virtual environment
    ```
    pipenv shell
    ```
1. Set the following environment variables in your shell:
   ```
   ENV=dev
   postgres_pwd=<YourPostgresDbPassword>
   ```
1. Run Flask application
    ```
    python app.py
    ```

### Package Management

To add new packages to the `pipenv` environment
```
pipenv install <package-name>
```
