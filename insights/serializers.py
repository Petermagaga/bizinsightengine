from rest_framework import serializers
from .models import Insight

class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model= Insight
        fields = ['id','dataset','content','created_at']

        