from rest_framework import serializers
from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Dataset
        fields =["id","name","file","uploaded_at"]
        read_only_fields= ["id",'uploaded_at']
    def validate_file(self,value):
        if not value.name.endswith(('.xlsx','.xls')):
            raise serializers.ValidationError("Only Excel files are allowed (.xlsx,xls)")
        return value