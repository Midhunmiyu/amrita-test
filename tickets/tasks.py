from celery import shared_task
from django.utils import timezone
from tickets.models import *
from django.db.models import Q


@shared_task
def create_employee_dutyroster():
    now = timezone.now()
    today = now.date()
    current_day = now.strftime("%A")
    if current_day == 'Sunday':
        return
    else:

        employees = Employee.objects.all()     
        for employee in employees:
            is_on_leave = Leave.objects.filter(employee=employee,start_date__lte=today,end_date__gte=today).exists()
            
            duty_roster_exists = DutyRoster.objects.filter(employee=employee, date=today).exists()
            shift = employee.employee_shifts.first() 
            if not duty_roster_exists and shift:
                duty = DutyRoster(
                    employee=employee,
                    date=today,
                    shift_start_time=shift.start_time,
                    shift_end_time=shift.end_time,
                    available=not is_on_leave  
                )
                duty.save()

        print('Duty roster creation completed for today.')