from rest_framework import serializers

from .models import *


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ('size', 'weight', 'price', 'available')


class PizzaToppingSerializer(serializers.HyperlinkedModelSerializer):
    pizzas = PizzaSerializer(many=True, read_only=True)

    class Meta:
        model = PizzaTopping
        fields = ('name', 'info', 'pizzas', 'slug')
