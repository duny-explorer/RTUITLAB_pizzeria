from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .paginations import *
from .serializers import *
from .models import *


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def list(self, request):
        p = request.GET.get('page')

        if p is not None:
            page = self.paginate_queryset(self.queryset)
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
