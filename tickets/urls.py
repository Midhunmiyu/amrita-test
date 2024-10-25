from django.urls import path
from tickets.views import *

urlpatterns = [
    path('employees/',EmployeeView.as_view(),name='employees'),
    path('tickets/',TicketView.as_view(),name='tickets')
]
