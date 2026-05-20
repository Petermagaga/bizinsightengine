from .views import (get_analysis,get_failed_rows,
                    dataset_status,dashboard_data)
from django.urls import path
from .trends_service import get_trends

urlpatterns = [
    path("<int:dataset_id>/analysis/",get_analysis),
    path("<int:dataset_id>v/failed/",get_failed_rows),
    path("<int:dataset_id>/status/",dataset_status),
    path(
        "<int:dataset_id>/dashboard/",
        dashboard_data
    ),
    path("<int:dataset_id>/trends/",get_trends)
]
