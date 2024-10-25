from rest_framework import serializers,status
from datetime import datetime
from django.utils import timezone
from tickets.models import *
from django.db.models import Q
from tickets.helpers import generate_ticket_number,get_next_employee

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
    assigned_employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = Ticket
        fields = ['id','ticket_number', 'description','assigned_employee', 'resolution_end_date']
        read_only_fields = ['ticket_number','assigned_employee']

    def validate(self,data):
        description = data.get('description')
        resolution_end_date = data.get('resolution_end_date')
        
        if not description:
            raise serializers.ValidationError('Please provide description...!!')
        
        if len(description) > 100:
            raise serializers.ValidationError('The length of the description has exceeded the maximum limit (100 characters)...!!')

        if not resolution_end_date:
            raise serializers.ValidationError('Please provide resolution end date...!!')

        if resolution_end_date and resolution_end_date < datetime.now().date():
            raise serializers.ValidationError('Resolution end date must be a future date...!!')
        return data

    def create(self, validated_data):
        description = validated_data.get('description')
        resolution_end_date = validated_data.get('resolution_end_date')

        # Generate ticket number
        ticket_number = generate_ticket_number()

        current_time = timezone.localtime(timezone.now()).time().replace(microsecond=0)
        today = timezone.now().date()
        #available employees - today for the current shift
        available_employees = (
            Employee.objects.filter(
                dutyrosters__date=today,
                dutyrosters__available=True,
                dutyrosters__shift_start_time__lte=current_time, 
                dutyrosters__shift_end_time__gte=current_time,
            ).distinct().order_by('id')
        )

        # Get the next employee
        next_employee = get_next_employee(available_employees)

        new_ticket = Ticket.objects.create(
            ticket_number=ticket_number,
            description=description,
            resolution_end_date=resolution_end_date,
            assigned_employee=next_employee
        )

        return new_ticket
    
class TicketUpdateSerializer(serializers.ModelSerializer):
    assigned_employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(),required=False)
    class Meta:
        model = Ticket
        fields = ['id','ticket_number','description','resolution_end_date','assigned_employee']

    def validate(self,data):
        # print(data)
        description = data.get('description')
        resolution_end_date = data.get('resolution_end_date')
        assigned_employee = data.get('assigned_employee')
        if not description and not self.instance.description:
            raise serializers.ValidationError('Please provide description...!!')
        
        if description and len(description) > 100:
            raise serializers.ValidationError('The length of the description has exceeded the maximum limit (100 characters)...!!')

        if not resolution_end_date and not self.instance.resolution_end_date:
            raise serializers.ValidationError('Please provide resolution end date...!!')

        if resolution_end_date and resolution_end_date < datetime.now().date():
            raise serializers.ValidationError('Resolution end date must be a future date...!!')
        if assigned_employee:
            try:
                employee = Employee.objects.get(id=assigned_employee.id)
            except Employee.DoesNotExist:
                raise serializers.ValidationError('Assigned employee not found...!!')
        return data


    def update(self, instance, validated_data):
        # print(validated_data,'validated_data***********')
        instance.description = validated_data.get('description', instance.description)
        instance.resolution_end_date = validated_data.get('resolution_end_date', instance.resolution_end_date)
        instance.assigned_employee = validated_data.get('assigned_employee', instance.assigned_employee)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['assigned_employee'] = EmployeeSerializer(instance.assigned_employee).data
        return representation
