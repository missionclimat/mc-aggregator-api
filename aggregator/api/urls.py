from django.urls import include, path
from rest_framework import routers
from api import views
from django.contrib import admin
from django.views.generic import TemplateView
# from rest_framework.schemas import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework.authtoken import views as authtoken_views

router = routers.DefaultRouter()
router.register(r"workshop", views.WorkshopViewSet, basename="Workshop")
router.register(r"result", views.ResultViewSet, basename="Result")

schema_view = get_schema_view(
   openapi.Info(
      title="aggregator-api",
      default_version='v1',
      description="The aggregator api is used to manage Workshop and results. This documentation is generated automatically and describe the routes available",
      contact=openapi.Contact(email="hugo.rochefort.pro@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-token-auth/', authtoken_views.obtain_auth_token, name="retrieve-token")

]
