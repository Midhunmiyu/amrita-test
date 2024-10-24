from tickets.serializers import *
from tickets.models import *
from rest_framework import status
from rest_framework.views import Response,APIView
from tickets.tasks import *


class EmployeeView(APIView):
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
        
