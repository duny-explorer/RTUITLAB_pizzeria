from rest_framework import serializers

from .models import *


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('pizza', 'quantity')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address', 'created', 'updated', 'paid', 'comment', 'total_cost',
                  'items')
