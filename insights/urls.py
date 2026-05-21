
from django.urls import path

from .views import (
    get_insights,
    dashboard_data,health_check
)

urlpatterns = [
    path(
        "<int:dataset_id>/",
        get_insights,
        name="get_insights"
    ),

    path(
        "dashboard/<int:dataset_id>/",
        dashboard_data,
        name="dashboard_data"
    ),
    path("health/",health_check,name="health_check")
]