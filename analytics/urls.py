from .views import get_analysis,FailedRow
from django.urls import path

urlpatterns = [
    path("<int: dataset_id>/",get_analysis),
    path("<int:dataset_id>/failed",FailedRow)
]
