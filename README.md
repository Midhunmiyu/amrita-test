# How to run

## 1.create a virtual environment
create a virtual environment and activate it using  the below commands
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
I use database PostgreSQL. Change the database settings as per yours


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
then import my database schema named amrita_test.sql to your database .After importing do migration command

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

Here i use celery for creating daily duty roster . I set the celery beat to create daily duty roster for all the employee by checking availability. 
```bash
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE= {
    'everyday-dutyroster':{
        'task':'tickets.tasks.create_employee_dutyroster',
        'schedule': crontab(hour=8, minute=0), #everyday 8am
    },
}
```
celery beat will run everyday morning 8AM (assuming the first shift starting from 9AM, so that it can check availability of employee before 1  hour of starting shift.)


