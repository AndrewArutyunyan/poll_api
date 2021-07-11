# Poll API

Django based REST API for polls. 

## Installation

1. Install and activate virtual environment (with virtualenv package for example).
2. Clone repository
3. Install all requirements from requirements.txt
4. Do migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Create a superuser:
```bash
python manage.py createsuperuser
```
Or you can use admin/admin user with DB from the repository
6. Run server:
```
python manage.py runserver
```

## Using API

Documentation on the polls api is provided at http://127.0.0.1:8000/docs

Automatically generated schema is provided at http://127.0.0.1:8000/schema

Api resources are at http://127.0.0.1:8000/api
