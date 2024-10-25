from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyUserManager(BaseUserManager):
    def create_user(self, email,name, password=None):
        """
        Creates and saves a User with the given emailand password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not name:
            raise ValueError("Users must have a name")

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=155)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Employee(models.Model):
    EDUCATION_CHOICE = {
        ('SSLC','SSLC'),
        ('12th','12th'),
        ('UG','UG'),
        ('PG','PG'),
    }
    GENDER_CHOICES = {
        ('Male','Male'),
        ('Female','Female'),

    }
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='employees')
    education = models.CharField(choices=EDUCATION_CHOICE,max_length=5,null=True,blank=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=6,null=True,blank=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    place = models.CharField(max_length=155,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name
    
class Shift(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='employee_shifts')
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee.user.name

class DutyRoster(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='dutyrosters')
    date = models.DateField(null=True,blank=True)
    shift_start_time = models.TimeField(null=True,blank=True)
    shift_end_time = models.TimeField(null=True,blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.user.name} on {self.date} - {'Available' if {self.available} else 'Unavailable'}"

class Leave(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='employee_leaves')
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.user.name} is leave from {self.start_date} to {self.end_date}"

class Ticket(models.Model):
    ticket_number = models.CharField(max_length=20,unique=True)
    description = models.TextField(null=True,blank=True)
    resolution_end_date = models.DateField(null=True,blank=True)
    assigned_employee = models.ForeignKey(Employee,on_delete=models.SET_NULL,related_name='employee_tickets', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket {self.ticket_number} - Assigned to {self.assigned_employee.user.name  if self.assigned_employee else 'Not Assigned'}"

