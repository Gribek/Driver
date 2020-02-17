# Driver

### Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

### General info
Driver is a REST API for a website on which various articles about road safety will be placed. The application is also intended to include tests to check the user's knowledge and the forum to ask questions. The API provides the back-end functionalities needed to run the application, includes an administration panel for content management (CRUD) and automatically generated endpoint documentation.

### Technologies
* Python 3.6.7
* Django 2.1.7
* Django REST framework 3.9.1
* PostgreSQL 10.10

### Setup
Fork and/or clone the repository to the selected folder using git clone command.

Create a virtual environment for the project, then activate it.
```
$ virtualenv -p python3 env
$ source env/bin/activate
```
Of course, you can also use IDE tools to configure the virtual environment.

Install dependencies.
```
$ pip install -r requirements.txt
```
Configure your database in settings.py. You must change values of NAME - database name, USER - postgresql user(role) and PASSWORD - user(role) password.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
    }
}
```
Execute the migration to the database.
```
$ python manage.py migrate
```
Run the application using the command:
```
$ python manage.py runserver
```
At the following address http://127.0.0.1:8000/swagger/ you will find a list of endpoints.

