from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from pizzeria.urls import router_pizzas
from orders.urls import router_orders
from rest_framework import routers


class DefaultsRouter(routers.DefaultRouter):
    trailing_slash = '/?'

    def extend(self, router):
        self.registry.extend(router.registry)


handler404 = lambda request, exception=None: JsonResponse({'status': '404',
                                                           'message': 'The resource was not found'}, status=404)

router = DefaultsRouter()
router.extend(router_orders)
router.extend(router_pizzas)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
