### Environment Setup
1. Install Python 3.9.7
    - On Windows, check the option to enable Python to be added to the PATH environment variable during installation. Otherwise, [add the path of Python to the PATH environment variable manually](https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/).
1. Create and activate a python environment (Optional)
    1. Using Conda
        ```
        conda create --name cloud python=3.9.7
        conda activate cloud
        ```
    1. Using venv
        ```
        # Mac bash
        source venv/Scripts/activate

        # Windows CMD
        venv\Scripts\activate
        ```
1. Install packages
    ```
    pip install -r requirements.txt
    ```
1. Start a shell in this project's root directory to run the backend
    1. Set the following environment variables in your shell:
        | Environment Variable Name | Value                 | Remarks |
        | ------------------------- | --------------------- | -------- |
        | FLASK_ENV                 | development           | Set this only if you are running the server locally |
        | postgres_pwd              | \<postgres password>  ||
        | ENV                       | "heroku" or "aws"     | Set this only on heroku or AWS |
    1. Create a PostgreSQL database and populate it following the steps in [docs/db-setup.md](docs/db-setup.md).
    1. Run the Flask backend
        ```
        flask run
        ```
        or
        ```
        python app.py
        ```
1. Start another shell in this project's root directory to run the frontend
    1. Change the current working directory to ./Frontend
    1. Follow the steps in [docs/frontend.md](docs/frontend.md)
