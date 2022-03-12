from django.urls import include, path
from rest_framework import routers
from . import views

router_orders = routers.DefaultRouter()
router_orders.register(r'orders', views.OrderViewSet, basename='orders')
