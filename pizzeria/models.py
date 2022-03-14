from django.db import models


class Pizza(models.Model):
    name = models.CharField(max_length=100, unique=True,  primary_key=True)
    info = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True, default="1", editable=False)

    def __str__(self):
        return self.name

    def save(self):
        self.slug = "_".join(self.name.lower().split())
        super(Pizza, self).save()


class Product(models.Model):
    PIZZA_SIZES = (
        ('25', '25cm'),
        ('30', '30cm'),
        ('35', '35cm'),
    )

    size = models.CharField(max_length=2, choices=PIZZA_SIZES)
    weight = models.IntegerField()
    pizza = models.ForeignKey(Pizza, related_name='products', on_delete=models.CASCADE)
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    pizza_slug = models.CharField(max_length=100, default="1", editable=False, unique=False)

    def __str__(self):
        return self.pizza.name + " " + self.size

    def save(self):
        self.pizza_slug = "_".join(self.pizza.name.lower().split())
        super(Product, self).save()

