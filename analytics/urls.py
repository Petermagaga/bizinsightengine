from .views import get_analysis,get_failed_rows
from django.urls import path

urlpatterns = [
    path("<int:dataset_id>/",get_analysis),
    path("<int:dataset_id>/failed/",get_failed_rows)
]
