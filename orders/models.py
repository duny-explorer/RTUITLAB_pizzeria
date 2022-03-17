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

    def total(self):
        return sum(item.get_cost() for item in self.items.all())

    def pre_add(self):
        self.total_cost = sum(item.get_cost() for item in self.items.all())

    def save(self,  *args, **kwargs):
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Product, related_name='+', on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.pizza.price * self.quantity

    def save(self, *args, **kwargs):
        super(OrderItem, self).save(*args, **kwargs)
