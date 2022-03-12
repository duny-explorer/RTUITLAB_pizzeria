from django.db import models
from pizzeria.models import *


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    comment = models.CharField(max_length=150)
    total_cost = models.IntegerField(default=1, editable=False)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def save(self):
        self.total_cost = sum(item.get_cost() for item in self.items.all())
        super(Order, self).save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, related_name='+', on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.pizza.price * self.quantity