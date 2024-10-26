from django.urls import path
from tickets.views import *

urlpatterns = [
    path('employees/',EmployeeView.as_view(),name='employees'),
    path('tickets/',TicketView.as_view(),name='tickets'),
    path('shifts/',ShiftView.as_view(),name='shifts'),
    path('leave/',LeaveView.as_view(),name='leave'),
    path('dutyroster/',DutyRosterView.as_view(),name='dutyroster'),
]
