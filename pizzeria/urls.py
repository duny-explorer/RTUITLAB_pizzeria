from django.urls import include, path
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedSimpleRouter
from . import views


router_pizzas = ExtendedSimpleRouter()
(
    router_pizzas.register(r'pizzas', views.PizzaViewSet, basename='pizzas')
        .register(r'products',
                  views.ProductViewSet,
                  basename='pizza-products',
                  parents_query_lookups=['pizza_slug'])
)
