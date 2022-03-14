from django.core.exceptions import FieldDoesNotExist
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .paginations import PizzaPagination
from rest_framework_extensions.mixins import NestedViewSetMixin
from .serializers import *
from .models import *


class ProductViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    model = Product


class PizzaViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    pagination_class = PizzaPagination
    lookup_field = 'slug'
    model = Pizza

    def list(self, request):
        p = request.GET.get('page')

        obj = self.queryset

        if p is not None:
            page = self.paginate_queryset(obj)
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
