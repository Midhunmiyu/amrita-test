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

class EmployeeCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    phone = serializers.CharField(write_only=True,required=False)
    gender = serializers.ChoiceField(choices=Employee.GENDER_CHOICES, write_only=True,required=False)
    education = serializers.ChoiceField(choices=Employee.EDUCATION_CHOICE, write_only=True,required=False)
    place = serializers.CharField(write_only=True,required=False)
    class Meta:
        model = CustomUser
        fields = ['id','email', 'name','password','password2','phone', 'gender', 'education', 'place']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')
        if not email and self.instance.email is None:
            raise serializers.ValidationError('Please provide an email address')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        if not name and self.instance.name is None:
            raise serializers.ValidationError('Please provide a name')
        if name and len(name) > 20:
            raise serializers.ValidationError('The length of the name has exceeded the maximum limit (20 characters)...!!')
        if not password and self.instance.password is None:
            raise serializers.ValidationError('Please provide a password')
        if password and len(password) > 8 :
            raise serializers.ValidationError('The length of the password has exceeded the minimum limit (8 characters)...!!')
        if not password2 and self.instance.password is None:
            raise serializers.ValidationError('Please confirm your password')
        if password != password2:
            raise serializers.ValidationError("Passwords didn't match")

        phone = data.get('phone')
        if phone and not phone.isdigit():
            raise serializers.ValidationError('The phone number must contain only digits')
        if phone and (len(phone) < 10 or len(phone) > 15):
            raise serializers.ValidationError('The phone number must be between 10 and 15 digits long')
        gender = data.get('gender')
        if gender and gender not in dict(Employee.GENDER_CHOICES).keys():
            raise serializers.ValidationError('Invalid gender provided')
        education = data.get('education')
        if education and education not in dict(Employee.EDUCATION_CHOICE).keys():
            raise serializers.ValidationError('Invalid education provided')
        return data
    
    def create(self, validated_data):
        name = validated_data.get('name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = CustomUser.objects.create_user(name=name,email=email,password=password)
        return user

    def update(self, instance, validated_data):
        name = validated_data.get('name',instance.name)
        gender = validated_data.get('gender')
        education = validated_data.get('education')
        place = validated_data.get('place')
        phone = validated_data.get('phone')
        instance.name = name
        instance.save()
        employee = Employee.objects.get(user=instance)
        employee.gender = gender
        employee.education = education
        employee.place = place
        employee.phone = phone
        employee.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = {
            "id": instance.id,
            "email": instance.email,
            "name": instance.name,
            "is_active": instance.is_active,
            "is_admin": instance.is_admin,
        }

        return {
            "id": instance.employees.id,
            "user": user_data,
            "gender": instance.employees.gender,
            "phone": instance.employees.phone,
            "place": instance.employees.place,
            "education": instance.employees.education
        }
        
    


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


class ShiftSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = Shift
        fields = ['id','employee','start_time','end_time','created_at','updated_at']


class ShiftCreateSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    class Meta:
        model = Shift
        fields = ['id','employee','start_time','end_time','created_at','updated_at']

    def validate(self,data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        employee = data.get('employee')
        if not employee and not self.instance.employee:
            raise serializers.ValidationError('Please provide employee...!!')
        if employee:
            try:
                employee_obj = Employee.objects.get(id=employee.id)

                if employee_obj is not None and start_time and end_time:
                    existing_shift = Shift.objects.filter(employee=employee_obj, start_time__lte=end_time, end_time__gte=start_time).exists()
                    if existing_shift:
                        raise serializers.ValidationError('Employee already has a shift during this time...!!')
            except Employee.DoesNotExist:
                raise serializers.ValidationError('Employee not found...!!')

        if not start_time and not self.instance.start_time:
            raise serializers.ValidationError('Please provide start time...!!')
        if not end_time and not self.instance.end_time:
            raise serializers.ValidationError('Please provide end time...!!')
        if start_time and end_time and start_time > end_time:
            raise serializers.ValidationError('Start time must be before end time...!!')
        return data
    
    def create(self,validated_data):
        start_time = validated_data.get('start_time')
        end_time = validated_data.get('end_time')
        employee = validated_data.get('employee')
        shift = Shift.objects.create(employee=employee,start_time=start_time,end_time=end_time)
        return shift
    
    def update(self,instance,validated_data):
        start_time = validated_data.get('start_time',instance.start_time)
        end_time = validated_data.get('end_time',instance.end_time)
        employee = validated_data.get('employee',instance.employee)
        instance.employee = employee
        instance.start_time = start_time
        instance.end_time = end_time
        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['employee'] = EmployeeSerializer(instance.employee).data
        return representation
    

class LeaveSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    class Meta:
        model = Leave
        fields = ['id','employee','start_date','end_date','created_at','updated_at']

class LeaveCreateSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    class Meta:
        model = Leave
        fields = ['id','employee','start_date','end_date','created_at','updated_at']

    def validate(self,data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        employee = data.get('employee')
        if not employee and not self.instance.employee:
            raise serializers.ValidationError('Please provide employee...!!')
        if employee:
            try:
                employee_obj = Employee.objects.get(id=employee.id)
            except Employee.DoesNotExist:
                raise serializers.ValidationError('Employee not found...!!')

        if not start_date and not self.instance.start_date:
            raise serializers.ValidationError('Please provide start date...!!')
        if not end_date and not self.instance.end_date:
            raise serializers.ValidationError('Please provide end date...!!')
        if start_date and end_date and start_date < end_date:
            raise serializers.ValidationError('End date must be the same as or after the start date...!!')

        if start_date and not end_date and self.instance:
            if start_date > self.instance.end_date:
                raise serializers.ValidationError('Start date cannot be after the existing end date...!!')

        if end_date and not start_date and self.instance:
            if end_date < self.instance.start_date:
                raise serializers.ValidationError('End date cannot be before the existing start date...!!')
        return data
    

    def create(self,validated_data):
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        employee = validated_data.get('employee')
        leave = Leave(employee=employee,start_date=start_date,end_date=end_date)
        leave.save()
        return leave
    
    def update(self,instance,validated_data):
        start_date = validated_data.get('start_date',instance.start_date)
        end_date = validated_data.get('end_date',instance.end_date)
        employee = validated_data.get('employee',instance.employee)
        instance.start_date = start_date
        instance.end_date=end_date
        instance.employee = employee
        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['employee'] = EmployeeSerializer(instance.employee).data
        return representation


class DutyRosterSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    class Meta:
        model = DutyRoster
        fields = ['id','employee', 'date', 'shift_start_time', 'shift_end_time', 'available', 'created_at']

class DutyRosterCreateSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    class Meta:
        model = DutyRoster
        fields = ['id','employee', 'date', 'shift_start_time', 'shift_end_time', 'available', 'created_at']

    def validate(self,data):
        employee = data.get('employee')
        date = data.get('date')
        shift_start_time = data.get('shift_start_time')
        shift_end_time = data.get('shift_end_time')
        available = data.get('available',True)
        if not date and not self.instance.date:
            raise serializers.ValidationError('Please provide date...!!')

        if not shift_start_time and not self.instance.shift_start_time:
            raise serializers.ValidationError('Please provide shift start time...!!')
        if not shift_end_time and not self.instance.shift_end_time:
            raise serializers.ValidationError('Please provide shift end time...!!')
        if shift_start_time and shift_end_time and shift_start_time > shift_end_time:
            raise serializers.ValidationError('Shift end time must be greater than the shift start time...!!')
        if available and available not in [True,False]:
            raise serializers.ValidationError('Available must be true or false...!!')
        if not employee and not self.instance.employee:
            raise serializers.ValidationError('Please provide employee...!!')
        if employee:
            try:
                employee_obj = Employee.objects.get(id=employee.id)
                if date and employee_obj.dutyrosters.filter(date=date).exists():
                    raise serializers.ValidationError('Employee already has a duty roster on this date...!!')
                
            except Employee.DoesNotExist:
                raise serializers.ValidationError('Employee not found...!!')
            
        return data
    
    def create(self,validated_data):
        employee = validated_data.get('employee')
        date = validated_data.get('date')
        shift_start_time = validated_data.get('shift_start_time')
        shift_end_time = validated_data.get('shift_end_time')
        available = validated_data.get('available')
        duty = DutyRoster(employee=employee,date=date,shift_start_time=shift_start_time,shift_end_time=shift_end_time,available=available if available else True)
        duty.save()
        return duty
    
    def update(self,instance,validated_data):
        employee = validated_data.get('employee',instance.employee)
        date = validated_data.get('date',instance.date)
        shift_start_time = validated_data.get('shift_start_time',instance.shift_start_time)
        shift_end_time = validated_data.get('shift_end_time',instance.shift_end_time)
        available = validated_data.get('available',instance.available)
        instance.employee = employee
        instance.date = date
        instance.shift_start_time = shift_start_time
        instance.shift_end_time = shift_end_time
        instance.available = available
        instance.save()
        return instance
        
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['employee'] = EmployeeSerializer(instance.employee).data
        return representation