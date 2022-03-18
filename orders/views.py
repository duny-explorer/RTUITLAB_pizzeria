from django.dispatch import receiver
from django.http import Http404
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from django.db.models.signals import post_save, post_delete
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.mixins import NestedViewSetMixin
from .paginations import *
from .serializers import *
from .models import *

import logging

logger = logging.getLogger(__name__)


class OrderItemViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']
    model = Order

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response({"status_code": 400, "message": "Empty body"}, status=status.HTTP_400_BAD_REQUEST)

        request.data._mutable = True
        request.data['order'] = self.get_parents_query_dict()['order_id']
        if 'pizza' in request.data and request.data['pizza']:
            pizza = request.data['pizza'].split()

            if len(pizza) == 2:
                request.data['pizza'] = Product.objects.get(pizza__name=pizza[0], size=pizza[1]).id

                if not request.data['pizza']:
                    return Response({"status_code": 400, "pizza": ["Incorrect name of pizza"]},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"status_code": 400, "pizza": ["Incorrect name of pizza"]},
                                status=status.HTTP_400_BAD_REQUEST)
        request.data._mutable = False
        return super(OrderItemViewSet, self).create(request, *args, **kwargs)

    def get_object(self):
        order = Order.objects.filter(id=self.get_parents_query_dict()['order_id'])

        if order:
            item = order[0].items.all()
            pk = int(self.kwargs['pk'])

            if len(item) < pk:
                raise Http404

            return item[pk - 1]

        raise Http404

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status_code': 404, 'message': "No content"}, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        if 'order' in request.data:
            request.data._mutable = True
            del request.data['order']
            request.data._mutable = False

        if 'pizza' in request.data:
            request.data._mutable = True
            del request.data['pizza']
            request.data._mutable = False


class OrderViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'first_name', 'last_name']
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']
    model = Order

    @method_decorator(cache_page(30))
    def list(self, request, *args, **kwargs):
        p = request.GET.get('page')

        if p is not None:
            page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
            serializer = self.get_serializer(page, many=True, context={"request": request})

            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(self.filter_queryset(self.get_queryset()),
                                             many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response({"status_code": 400, "message": "Empty body"}, status=status.HTTP_400_BAD_REQUEST)

        return super(OrderViewSet, self).create(request, *args, **kwargs)


@receiver(post_save, sender=OrderItem)
def post_save_item(sender, instance, *args, **kwargs):
    order = Order.objects.get(id=slugify(instance.order_id))
    order.total_cost = order.total()
    order.save()


@receiver(post_delete, sender=OrderItem)
def post_delete_item(sender, instance, *args, **kwargs):
    order = Order.objects.get(id=slugify(instance.order_id))
    order.total_cost = order.total()
    order.save()
