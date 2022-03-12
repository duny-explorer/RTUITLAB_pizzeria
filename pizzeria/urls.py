from django.urls import include, path
from rest_framework import routers
from . import views

router_pizzas = routers.DefaultRouter()
router_pizzas.register(r'pizzas', views.PizzaViewSet, basename='pizzas')
