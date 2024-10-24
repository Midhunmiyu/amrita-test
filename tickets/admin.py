from django.contrib import admin
from tickets.models import *


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id','email','name','is_active','is_admin']
    search_fields = ['email','name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id','user','gender','phone','education','place','created_at','updated_at']

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['id','employee','start_time','end_time','created_at','updated_at']

@admin.register(DutyRoster)
class DutyRosterAdmin(admin.ModelAdmin):
    list_display = ['id','employee','date','shift_start_time','shift_end_time','available','created_at','updated_at']


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['id','employee','start_date','end_date','created_at','updated_at']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id','ticket_number', 'description', 'resolution_end_date', 'assigned_employee', 'created_at', 'updated_at']
