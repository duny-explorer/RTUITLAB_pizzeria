from django.dispatch import receiver
from django.http import Http404
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from django.db.models.signals import pre_save, post_save, post_delete
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
    model = Order

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response({"status": "400", "message": "Empty body"}, status=status.HTTP_400_BAD_REQUEST)

        request.data._mutable = True
        request.data['order'] = self.get_parents_query_dict()['order_id']
        request.data._mutable = False
        return super(OrderItemViewSet, self).create(request, *args, **kwargs)

    def get_object(self):
        item = Order.objects.get(id=self.get_parents_query_dict()['order_id']).items.all()
        pk = int(self.kwargs['pk'])

        if len(item) < pk:
            raise Http404

        return item[pk - 1]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': '404', 'message': "No content"}, status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'first_name', 'last_name']
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
            return Response({"status": "400", "message": "Empty body"}, status=status.HTTP_400_BAD_REQUEST)

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
