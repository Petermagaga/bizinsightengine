from django.urls import path
from .views import (upload_dataset,
                     dataset_status,
                     list_datasets)

urlpatterns = [
    path("",list_datasets),
    path("upload/", upload_dataset),
    path("<int:dataset_id>/status/", dataset_status),
]