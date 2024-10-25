from django.utils import timezone
from datetime import datetime
from tickets.models import *



def generate_ticket_number(prefix = "ASF"):

    today_str = datetime.now().strftime("%d%m%Y")  

    last_ticket = Ticket.objects.filter(
        created_at__date=datetime.now().date()
    ).order_by('created_at').last()

    if last_ticket and last_ticket.ticket_number.startswith(prefix + today_str):
        last_counter = int(last_ticket.ticket_number[-3:])  # Get the last 3 digits
        new_counter = last_counter + 1
    else:
        new_counter = 1 
    
    # Generate ticket number like ASF12042024001
    ticket_number = f"{prefix}{today_str}{new_counter:03}" 
    return ticket_number


def get_next_employee(available_employees):
    today = timezone.now().date()
    employees_list = list(available_employees)
    last_assigned_ticket = Ticket.objects.filter(
        assigned_employee__in=available_employees, created_at__date=today
    ).order_by('-created_at').first()

    if last_assigned_ticket and available_employees.exists():
        last_employee_id = last_assigned_ticket.assigned_employee.id
        last_index = [emp.id for emp in employees_list].index(last_employee_id)
        next_index = (last_index + 1) % len(employees_list)
        next_employee = employees_list[next_index]
    else:
        next_employee = employees_list[0] if employees_list else None
    return next_employee