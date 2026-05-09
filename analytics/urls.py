from .views import get_analysis
from django.urls import path

urlpatterns = [
    path("<int: dataset_id>/",get_analysis),
]
