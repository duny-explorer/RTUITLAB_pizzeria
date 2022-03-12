from django.db import models


class PizzaTopping(models.Model):
    name = models.CharField(max_length=100, unique=True)
    info = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True, default="1", editable=False)

    def __str__(self):
        return self.name

    def save(self):
        self.slug = "_".join(self.name.lower().split())
        super(PizzaTopping, self).save()


class Pizza(models.Model):
    PIZZA_SIZES = (
        ('25', '25cm'),
        ('30', '30cm'),
        ('35', '35cm'),
    )

    size = models.CharField(max_length=2, choices=PIZZA_SIZES)
    weight = models.IntegerField()
    topping = models.ForeignKey(PizzaTopping, related_name='pizzas', on_delete=models.CASCADE)
    price = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.topping.name + " " + self.size
