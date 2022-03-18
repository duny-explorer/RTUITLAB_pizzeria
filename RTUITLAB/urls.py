from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pizzeria.urls import router_pizzas
from orders.urls import router_orders

from rest_framework import routers, status

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


class DefaultsRouter(routers.DefaultRouter):
    trailing_slash = '/?'

    def extend(self, router):
        self.registry.extend(router.registry)


@api_view()
def health(request):
    """
    return status 200
    """
    return Response({'status_code': '200', 'message': 'OK'},
                    status=status.HTTP_200_OK)


@api_view()
def version(request):
    """
    return version of API
    """
    return Response({'status_code': '200', 'message': '1.0.0'},
                    status=status.HTTP_200_OK)


handler404 = lambda request, exception=None: JsonResponse({'status_code': '404',
                                                           'message': 'The resource was not found'},
                                                          status=status.HTTP_404_NOT_FOUND)

router = DefaultsRouter()
router.extend(router_orders)
router.extend(router_pizzas)

urlpatterns = [
    path('health', health, name='health'),
    path('version', version, name='version'),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
