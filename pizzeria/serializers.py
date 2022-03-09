from rest_framework import serializers

from .models import *


class PizzaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pizza
        fields = ('name', 'size', 'price', 'weight', 'ingredients', 'available')
