from faker import Faker
from tickets.models import CustomUser
from time import sleep

fake = Faker()

def generate_user():
    for i in range(10):
        email = fake.email()
        name = fake.name()
        password = '12'
        CustomUser.objects.create_user(email=email,name=name,password=password)
        sleep(2)
    print('Employees Created...!!!!')