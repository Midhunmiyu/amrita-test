from tickets.serializers import *
from tickets.models import *
from rest_framework import status
from rest_framework.views import Response,APIView
from tickets.tasks import *
from tickets.renderers import *
from tickets.mypagination import MyPaginations


#employee
class EmployeeView(APIView):
    renderer_classes = [CustomRenderer]

    def get(self,request):

        try:
            employee_id = request.query_params.get('employee_id')
            if employee_id:
                try:
                    employee = Employee.objects.get(id=employee_id)
                    serializers = EmployeeSerializer(employee)
                    return Response({'status':'success','message':'Employee data retrieved successfully','data':serializers.data},status=status.HTTP_200_OK)
                except Employee.DoesNotExist :
                    return Response({'status':'error','message':'Employee not found...!!'},status=status.HTTP_400_BAD_REQUEST)
            employees = Employee.objects.all().order_by('-id')
            if employees.exists():
                paginator = MyPaginations()
                paginated_employees = paginator.paginate_queryset(employees, request)
                serializer = EmployeeSerializer(paginated_employees,many=True)
                response_data = {
                    'status': 'success',
                    'message': 'Employees data retrieved successfully',
                    'data': serializer.data, 
                    'count': paginator.page.paginator.count, 
                    'next': paginator.get_next_link(), 
                    'previous': paginator.get_previous_link(),
                }
                return Response(response_data,status=status.HTTP_200_OK)
            else:
                return Response({'status':'Success','message':'No employee record found'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self,request):
        try:
            data = request.data
            serializers = EmployeeCreateSerializer(data=data)
            if serializers.is_valid():
                serializers.save()
                return Response({'status':'success','message':'Employee created successfully','data':serializers.data},status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self,request):
        try:
            employee_id = request.query_params.get('employee_id')
            data=request.data
            user = CustomUser.objects.get(id=employee_id)
            serializer = EmployeeCreateSerializer(user,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':'success','message':'Employee data updated successfully','data':serializer.data},status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        try:
            employee_id = request.query_params.get('employee_id')
            user = CustomUser.objects.get(id=employee_id)
            user.delete()
            return Response({'status':'success','message':'Employee deleted successfully'},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#ticket
class TicketView(APIView):
    renderer_classes = [CustomRenderer]

    def get(self,request):
        try:
            ticket_id = request.query_params.get('ticket_id')
            if ticket_id:
                try:
                    ticket = Ticket.objects.get(id=ticket_id)
                    serializers = TicketSerializer(ticket)
                    return Response({'status':'success','message':'Ticket data retrieved successfully','data':serializers.data},status=status.HTTP_200_OK)
                except Ticket.DoesNotExist :
                    return Response({'status':'error','message':'Ticket not found...!!'},status=status.HTTP_400_BAD_REQUEST)
            tickets = Ticket.objects.all().order_by('-id')
            paginator = MyPaginations()
            paginated_tickets = paginator.paginate_queryset(tickets, request)
            serializer = TicketSerializer(paginated_tickets,many=True)
            response_data = {
                'status': 'success',
                'message': 'Tickets data retrieved successfully',
                'data': serializer.data, 
                'count': paginator.page.paginator.count, 
                'next': paginator.get_next_link(), 
                'previous': paginator.get_previous_link(),
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        try:
            data = request.data
            serializers = TicketCreateSerializer(data=data)
            if serializers.is_valid():
                serializers.save()
                return Response({'status':'success','message':'Ticket created successfully','data':serializers.data},status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self,request):
        try:
            data = request.data
            ticket_id = request.query_params.get('ticket_id')
            try:
                ticket = Ticket.objects.get(id=ticket_id)
                serializers = TicketUpdateSerializer(ticket,data=data,partial=True)
                if serializers.is_valid():
                    serializers.save()
                    return Response({'status':'success','message':'Ticket updated successfully','data':serializers.data},status=status.HTTP_200_OK)
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            except Ticket.DoesNotExist :
                return Response({'status':'error','message':'Ticket not found...!!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request):
        try:
            ticket_id = request.query_params.get('ticket_id')
            try:
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.delete()
                return Response({'status':'success','message':'Ticket deleted successfully'},status=status.HTTP_200_OK)
            except Ticket.DoesNotExist :
                return Response({'status':'error','message':'Ticket not found...!!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Shift
class ShiftView(APIView):
    renderer_classes = [CustomRenderer]
    def get(self,request):
        try:
            shift_id = request.query_params.get('shift_id')
            if shift_id:
                try:
                    shift = Shift.objects.get(id=shift_id)
                    serializers = ShiftSerializer(shift)
                    return Response({'status':'success','message':'Shift data retrieved successfully','data':serializers.data},status=status.HTTP_200_OK)
                except Shift.DoesNotExist :
                    return Response({'status':'error','message':'Shift not found...!!'},status=status.HTTP_400_BAD_REQUEST)
            shifts = Shift.objects.all().order_by('-id')
            if shifts.exists():
                paginator = MyPaginations()
                paginated_shifts = paginator.paginate_queryset(shifts, request)
                serializers = ShiftSerializer(paginated_shifts,many=True)
                response_data = {
                    'status': 'success',
                    'message': 'Shifts data retrieved successfully',
                    'data': serializers.data, 
                    'count': paginator.page.paginator.count, 
                    'next': paginator.get_next_link(), 
                    'previous': paginator.get_previous_link(),
                }
                return Response(response_data,status=status.HTTP_200_OK)
            else:
                return Response({'status':'Success','message':'No shift record found'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self,request):
        try:
            data = request.data
            serializers = ShiftCreateSerializer(data=data)
            if serializers.is_valid():
                serializers.save()
                return Response({'status':'success','message':'Shift created successfully','data':serializers.data},status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self,request):
        try:
            data = request.data
            shift_id = request.query_params.get('shift_id')
            try:
                shift = Shift.objects.get(id=shift_id)
                serializers = ShiftCreateSerializer(shift,data=data,partial=True)
                if serializers.is_valid():
                    serializers.save()
                    return Response({'status':'success','message':'Shift updated successfully','data':serializers.data},status=status.HTTP_200_OK)
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            except Shift.DoesNotExist :
                return Response({'status':'error','message':'Shift not found...!!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        try:
            shift_id = request.query_params.get('shift_id')
            try:
                shift = Shift.objects.get(id=shift_id)
                shift.delete()
                return Response({'status':'success','message':'Shift deleted successfully'},status=status.HTTP_200_OK)
            except Shift.DoesNotExist :
                return Response({'status':'error','message':'Shift not found...!!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#leave
class LeaveView(APIView):
    renderer_classes = [CustomRenderer]
    def get(self,request):
        try:
            leave_id = request.query_params.get('leave_id')
            if leave_id:
                try:
                    leave = Leave.objects.get(id=leave_id)
                    serializers = LeaveSerializer(leave)
                    return Response({'status':'success','message':'Leave data retrieved successfully','data':serializers.data},status=status.HTTP_200_OK)
                except Leave.DoesNotExist :
                    return Response({'status':'error','message':'Leave not found...!!'},status=status.HTTP_400_BAD_REQUEST)
            leaves = Leave.objects.all().order_by('-id')
            if leaves.exists():
                paginator = MyPaginations()
                paginated_leaves = paginator.paginate_queryset(leaves, request)
                serializers = LeaveSerializer(paginated_leaves,many=True)
                response_data = {
                    'status': 'success',
                    'message': 'Employees leave data retrieved successfully',
                    'data': serializers.data, 
                    'count': paginator.page.paginator.count, 
                    'next': paginator.get_next_link(), 
                    'previous': paginator.get_previous_link(),
                }
                return Response(response_data,status=status.HTTP_200_OK)
            else:
                return Response({'status':'Success','message':'No leave record found'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self,request):
        try:
            data = request.data
            serializers = LeaveCreateSerializer(data=data)
            if serializers.is_valid():
                serializers.save()
                return Response({'status':'success','message':'Leave created successfully','data':serializers.data},status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self,request):
        try:
            data = request.data
            leave_id = request.query_params.get('leave_id')
            try:
                leave = Leave.objects.get(id=leave_id)
                serializers = LeaveCreateSerializer(leave,data=data,partial=True)
                if serializers.is_valid():
                    serializers.save()
                    return Response({'status':'success','message':'Leave updated successfully','data':serializers.data},status=status.HTTP_200_OK)
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            except Leave.DoesNotExist :
                return Response({'status':'error','message':'Leave not found...!!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        try:
            leave_id = request.query_params.get('leave_id')
            try:
                leave = Leave.objects.get(id=leave_id)
                leave.delete()
                return Response({'status':'success','message':'Leave deleted successfully'},status=status.HTTP_200_OK)
            except Leave.DoesNotExist :
                return Response({'status':'error','message':'Leave not found...!!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#Dutyroster
class DutyRosterView(APIView):
    renderer_classes = [CustomRenderer]
    def get(self,request):
        try:
            duty_roster_id = request.query_params.get('duty_roster_id')
            if duty_roster_id:
                try:
                    duty_roster = DutyRoster.objects.get(id=duty_roster_id)
                    serializers = DutyRosterSerializer(duty_roster)
                    return Response({'status':'success','message':'Duty roster data retrieved successfully','data':serializers.data},status=status.HTTP_200_OK)
                except DutyRoster.DoesNotExist :
                    return Response({'status':'error','message':'Duty roster not found...!!'},status=status.HTTP_400_BAD_REQUEST)
            duty_rosters = DutyRoster.objects.all().order_by('-id')
            if duty_rosters.exists():
                paginator = MyPaginations()
                paginated_duty_rosters = paginator.paginate_queryset(duty_rosters, request)
                serializers = DutyRosterSerializer(paginated_duty_rosters,many=True)
                response_data = {
                    'status': 'success',
                    'message': 'Duty roster data retrieved successfully',
                    'data': serializers.data, 
                    'count': paginator.page.paginator.count, 
                    'next': paginator.get_next_link(), 
                    'previous': paginator.get_previous_link(),
                }
                return Response(response_data,status=status.HTTP_200_OK)
            else:
                return Response({'status':'Success','message':'No duty roster record found'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self,request):
        try:
            data = request.data
            serializers = DutyRosterCreateSerializer(data=data)
            if serializers.is_valid():
                serializers.save()
                return Response({'status':'success','message':'Duty roster created successfully','data':serializers.data},status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self,request):
        try:
            data = request.data
            duty_roster_id = request.query_params.get('duty_roster_id')
            try:
                duty_roster = DutyRoster.objects.get(id=duty_roster_id)
                serializers = DutyRosterCreateSerializer(duty_roster,data=data,partial=True)
                if serializers.is_valid():
                    serializers.save()
                    return Response({'status':'success','message':'Duty roster updated successfully','data':serializers.data},status=status.HTTP_200_OK)
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            except DutyRoster.DoesNotExist :
                return Response({'status':'error','message':'Duty roster not found...!!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        try:
            duty_roster_id = request.query_params.get('duty_roster_id') 
            try:
                duty_roster = DutyRoster.objects.get(id=duty_roster_id)
                duty_roster.delete()
                return Response({'status':'success','message':'Duty roster deleted successfully'},status=status.HTTP_200_OK)
            except DutyRoster.DoesNotExist :
                return Response({'status':'error','message':'Duty roster not found...!!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)