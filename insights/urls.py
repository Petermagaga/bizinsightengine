from django.urls import path
from .views import get_insights

urlpatterns = [
    path("<int:dataset_id>/insights/",get_insights),
]
