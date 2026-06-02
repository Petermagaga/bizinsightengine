
from django.urls import path

from .views import (
    get_insights,
    dashboard_data,health_check,
    ask_dataset
)

urlpatterns = [
    path(
        "insights/<int:dataset_id>/",
        get_insights,
        name="get_insights"
    ),

    path(
        "insights/dashboard/<int:dataset_id>/",
        dashboard_data,
        name="dashboard_data"
    ),
    path("health/",health_check,name="health_check"),
    path(
    "chat/<int:dataset_id>/",
    ask_dataset
)
]