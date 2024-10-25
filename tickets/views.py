from tickets.serializers import *
from tickets.models import *
from rest_framework import status
from rest_framework.views import Response,APIView
from tickets.tasks import *
from tickets.renderers import *
from tickets.mypagination import MyPaginations


class EmployeeView(APIView):
    renderer_classes = [CustomRenderer]

    def get(self,request):
        try:
            employees = Employee.objects.all()
            if employees.exists():
                serializers = EmployeeSerializer(employees,many=True)
                return Response({'status':'success','message':'Employee data retrieved successfully','data':serializers.data},status=status.HTTP_200_OK)
            else:
                return Response({'status':'Success','message':'No employee record found'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

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


