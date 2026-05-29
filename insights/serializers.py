from rest_framework import serializers
from .models import Insight

class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model= Insight
        fields = ['id',
                  'dataset',
                  "summary_text",
                  'bi_insights',
                  'predictions',
                  'created_at']

