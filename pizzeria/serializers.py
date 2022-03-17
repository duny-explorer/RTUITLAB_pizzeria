from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('size', 'weight', 'price', 'available', 'pizza')
        validators = [
            UniqueTogetherValidator(
                queryset=Product.objects,
                fields=['size', 'pizza']
            )]

    def create(self, validated_data):
        return Product.objects.create(**validated_data)


class PizzaSerializer(serializers.HyperlinkedModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Pizza
        fields = ('name', 'info', 'products', 'slug')

    def create(self, validated_data):
        return Pizza.objects.create(**validated_data)
