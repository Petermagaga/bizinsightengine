from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def test_api(request):
    return Response({"message":"API working"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test/',test_api),
    path('api/data/',include('data_ingestion.urls')),
    path('api/v1/insights/',include('insights.urls')),
    path('api/auth/',include('users.urls')),
    path('api/analytics/',include("analytics.urls"))
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)