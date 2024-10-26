# How to run

## 1.create a virtual environment
Create a virtual environment and activate it using the commands provided below.
```bash
py -m venv venv

source venv/Scripts/activate
```
## 2.clone the project
```bash
git clone https://github.com/Midhunmiyu/amrita-test.git

cd amrita-test/
```

## 3.Installation

```bash
pip install -r requirements.txt
```

## 4.Database
I use PostgreSQL as my database. Please adjust the database settings accordingly to match your configuration.


```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'amrita_test',
        'USER': 'postgres',
        'PASSWORD': '8157',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
```
Next, import my database schema file named amrita_test.sql into your database. After the import, run the migration command.

```bash
python manage.py migrate
```
## 4.Run project
```python
python manage.py runserver

# open another terminal for celery worker
celery -A employee_management worker --pool=solo -l INFO


# open another terminal for celery beat
celery -A employee_management beat -l INFO

```

## Celery

I use Celery to create a daily duty roster. I've configured Celery Beat to generate the roster for all employees by checking their availability. 
```bash
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE= {
    'everyday-dutyroster':{
        'task':'tickets.tasks.create_employee_dutyroster',
        'schedule': crontab(hour=8, minute=0), #everyday 8am
    },
}
```
Celery Beat will run every day at 8 AM, allowing it to check employee availability one hour before the first shift starts at 9 AM. (assuming the first shift starting from 9AM)

## Test API
I've provided the Postman collections file for you. You can import it into Postman to test the API.
