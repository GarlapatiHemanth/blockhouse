# Blockhouse

#### This is a Django project that does fetching,predicting,backtracking of stocks. Below are the steps to set up and run the project locally.

### Table of Contents

1. Cloning the Repository
2. Setting Up the Environment
3. Installing Dependencies
4. Configurations
5. DataBase Setup
6. Running Migrations
7. Starting the Server
8. Api overview
9. Url Construction


### Cloning the Repository

    To get started, first clone the repository from GitHub to your local machine:
    git clone https://github.com/GarlapatiHemanth/blockhouse.git
    After cloning, navigate into the project directory

### Setting Up the Environment

    you can check the python --version to verify python installed in the system
    Before proceeding, make sure you have Python installed on your system. It’s recommended to use a virtual environment to manage dependencies.

### Installing Dependencies

    Install the required Python packages listed in the app/requirements.txt file:
    pip install -r /app/requirements.txt

### Configurations

    --configuration=Dev for dev environment
    --configuration=Prod for Prod environment

    you need to include the api key in settings.py to access Alpha Vantage API's

### DataBase setup

    Postgress Sql database has been used
    
    Local : To run this you need to have this database setup in local and details need to be mentioned in setting.py under class Dev or you can use inbuilt sqlite database that comes with Django

    server : postgress database has been setup in nexon
    https://console.neon.tech/app/projects/spring-silence-75927059/query?branchId=br-crimson-darkness-a53c0n0l&database=blockhouse_db

### Running Migrations

    Before starting the server, you'll need to apply the migrations to set up the database. Run the following command:
    python manage.py migrate --configuration=Dev
    This command will execute the necessary migrations to create database tables for your Django application.

### Starting the Server

    Once the migrations are complete, start the Django development server:

    python manage.py runserver --configuration=Dev

    The application will be accessible at http://127.0.0.1:8000/ in your web browser/postman.

    Currently ci-cd pipeline is integrated in .githud/workflow to automatically deploy from main branch of github
### Api overview
    There are four api's

    fetch_data- to fetch data. extension is /app/fetch
    run_backtest - to run the backtest. extension is /app/backtest
    predict_stock_prices - to predict and store the 30 days stock prices. extension is /app/predict
    report - to get the report. It has one additional parameter 'f' based on the value it return json or pdf response. Default value is json. f=pdf return pdf report. Extension is app/report

    These application has been deployed in Render and can be accessable by url
    https://blockhouse-latest.onrender.com/

### Url Construction-

    local : http://127.0.0.1:8000/ + extension -> http://127.0.0.1:8000/fetch for fetch api and similar for other api's

    server : https://blockhouse-latest.onrender.com/ + extension -> https://blockhouse-latest.onrender.com/fetch for fetch api and similar for other api's




