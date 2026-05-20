from django.urls import path
from .views import get_insights,dashboard_data

urlpatterns = [
    path("<int:dataset_id>/",get_insights),
    path("<int:dataset_id>/dashboard/",dashboard_data),
]
