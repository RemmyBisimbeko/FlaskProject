# FlaskProject
My first Flask Project

# Instation
$ brew install python3
$ pip install Flask

# Initialization
$ Flask run

# Rename api_app
Rename api_app.py to app.py to access Restful API codebase


# REST API With Flask & SQL Alchemy

> loans API using Python Flask, SQL Alchemy and Marshmallow

## Quick Start Using Pipenv

``` bash
# Activate venv
$ pipenv shell

# Install dependencies
$ pipenv install

# Create DB
$ python
>> from app import db
>> db.create_all()
>> exit()

# Run Server (http://localhst:5000)
python app.py
```

## Endpoints

* GET     /loan
* GET     /loan/:id
* POST    /loan
* PUT     /loan/:id
* DELETE  /loan/:id

## UI-SQL
# Install pip

# Install flask
$ pip install Flask
