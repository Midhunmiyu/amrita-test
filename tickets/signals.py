from django.db.models.signals import post_save
from django.dispatch import receiver
from tickets.models import *


@receiver(post_save,sender=CustomUser)
def create_employee(sender,instance,created,**kwargs):
    if created and not instance.is_admin:
        print('User created')
        Employee.objects.create(user=instance)

