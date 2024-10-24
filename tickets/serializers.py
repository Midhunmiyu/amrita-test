from rest_framework import serializers,status
from tickets.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','name','is_active','is_admin']

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Employee
        fields = ['id','user','phone','gender','education','place','created_at','updated_at']

class TicketSerializer(serializers.ModelSerializer):
    assigned_employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = Ticket
        fields = ['id','ticket_number','description','resolution_end_date','assigned_employee','created_at','updated_at']


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id','ticket_number', 'description', 'resolution_end_date']