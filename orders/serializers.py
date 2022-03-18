from rest_framework import serializers

from .models import *


class ItemSerializer(serializers.ModelSerializer):
    #pizza = serializers.CharField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('pizza', 'quantity', 'order')

    def create(self, validated_data):
        return OrderItem.objects.create(**validated_data)


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address', 'created', 'updated', 'paid', 'comment', 'total_cost',
                  'items')

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
