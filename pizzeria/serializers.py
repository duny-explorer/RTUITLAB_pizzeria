from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('size', 'weight', 'price', 'available', 'pizza')


class PizzaSerializer(serializers.HyperlinkedModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Pizza
        fields = ('name', 'info', 'products', 'slug')
