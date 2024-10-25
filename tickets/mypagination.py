from rest_framework.pagination import PageNumberPagination

class MyPaginations(PageNumberPagination):
    page_size = 2
