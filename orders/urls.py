from rest_framework_extensions.routers import ExtendedSimpleRouter
from . import views


router_orders = ExtendedSimpleRouter()
(
    router_orders.register(r'orders', views.OrderViewSet, basename='orders')
        .register(r'items',
                  views.OrderItemViewSet,
                  basename='order_items',
                  parents_query_lookups=['order_id'])
)
