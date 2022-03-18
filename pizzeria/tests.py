from django.test import TestCase
from .models import *
from django.test.client import Client


class PizzaApiTestCase(TestCase):
    def setUp(self):
        Pizza.objects.create(name="Peperoni", info="like italian")
        Pizza.objects.create(name="Carbonara", info="It isn't pasta, is pizza")
        Product.objects.create(size='25', weight='100', pizza=Pizza.objects.get(name='Peperoni'), price=10)
        Product.objects.create(size='30', weight='110', pizza=Pizza.objects.get(name='Peperoni'), price=12)
        Product.objects.create(size='25', weight='110', pizza=Pizza.objects.get(name='Carbonara'), price=15)

    def test_str_product(self):
        self.assertEqual(str(Product.objects.get(id=1)), 'Peperoni 25')
        self.assertEqual(str(Product.objects.get(id=2)), 'Peperoni 30')
        self.assertEqual(str(Product.objects.get(id=3)), 'Carbonara 25')

    def test_add_api_pizza(self):
        c = Client()
        response = c.post('/pizzas/', {'name': 'Mushrooms and bacon', 'info': 'MMMMM'})
        self.assertEqual(response.status_code, 403)

        log = c.login(Username='duny', Password='duny')
        response = c.post('/pizzas/', {'name': 'Mushrooms and bacon', 'info': 'MMMMM'})
        self.assertEqual(response.status_code, 200)



