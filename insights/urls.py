
from django.urls import path

from .views import (
    get_insights,
    dashboard_data
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
]