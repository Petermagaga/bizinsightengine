from rest_framework import serializers
from .models import Dataset


class DatasetSerializer(serializers.Serializer):
    class Meta:
        model=Dataset
        fields =["id","name","file","uploaded_at"]
        read_only_fields= ["id",'uploaded_at']
        