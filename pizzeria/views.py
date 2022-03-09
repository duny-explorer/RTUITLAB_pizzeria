from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .paginations import PizzaPagination
from .serializers import PizzaSerializer
from .models import Pizza


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all().order_by('name')
    serializer_class = PizzaSerializer
    pagination_class = PizzaPagination

    def list(self, request):
        queryset = Pizza.objects.all()
        page = request.GET.get('page')

        if page is not None:
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = PizzaSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
