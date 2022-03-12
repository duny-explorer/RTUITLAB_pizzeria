from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .paginations import PizzaPagination
from .serializers import *
from .models import *

import logging
logger = logging.getLogger(__name__)


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = PizzaTopping.objects.all()
    serializer_class = PizzaToppingSerializer
    pagination_class = PizzaPagination
    lookup_field = 'slug'

    def list(self, request):
        p = request.GET.get('page')

        if p is not None:
            page = self.paginate_queryset(self.queryset)
            serializer = self.get_serializer(page, many=True)

            if p == "2":
                logger.error(serializer.data[0])

            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
