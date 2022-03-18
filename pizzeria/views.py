from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.response import Response
from .paginations import PizzaPagination
from rest_framework_extensions.mixins import NestedViewSetMixin
from .serializers import *
from .models import *

import logging
logger = logging.getLogger(__name__)


class ProductViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    model = Product
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response({"status_code": 400, "message": "Empty body"}, status=status.HTTP_400_BAD_REQUEST)

        if 'pizza' in request.data:
            pizza = Pizza.objects.get(slug=self.get_parents_query_dict()['pizza_slug']).name

            request.data._mutable = True
            request.data['pizza'] = pizza
            request.data._mutable = False
        return super(ProductViewSet, self).create(request, *args, **kwargs)

    def get_object(self):
        pizza = Pizza.objects.filter(slug=self.get_parents_query_dict()['pizza_slug'])

        if pizza:
            product = pizza[0].products.all()
            pk = int(self.kwargs['pk'])

            if len(product) < pk or not product:
                raise Http404

            return product[pk - 1]

        raise Http404

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status_code': 404, 'message': "No content"}, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        if 'pizza' in request.data:
            request.data._mutable = True
            del request.data['pizza']
            request.data._mutable = False


class PizzaViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    pagination_class = PizzaPagination
    lookup_field = 'slug'
    model = Pizza
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        p = request.GET.get('page')

        obj = self.queryset

        if p is not None:
            page = self.paginate_queryset(obj)
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response({"status_code": 400, "message": "Empty body"}, status=status.HTTP_400_BAD_REQUEST)

        return super(PizzaViewSet, self).create(request, *args, **kwargs)
