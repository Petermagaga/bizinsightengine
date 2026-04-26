from django.urls import path
from .views import register_user
from rest_framework_simplejwt.

urlpatterns = [
    path("register/",register_user),
]
