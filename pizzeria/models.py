from django.db import models


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    price = models.IntegerField()
    weight = models.IntegerField()
    ingredients = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

