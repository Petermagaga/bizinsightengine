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






from rest_framework import serializers


class DashboardSerializer(
    serializers.Serializer
):
    kpis = serializers.DictField()

    production_chart = (
        serializers.ListField()
    )

    forecast_chart = (
        serializers.ListField()
    )

    time_series = (
        serializers.ListField()
    )

    trend_summary = (
        serializers.DictField()
    )

    business_health = (
        serializers.CharField()
    )

    summary = (
        serializers.DictField(
            required=False
        )
    )

    alerts = (
        serializers.ListField(
            required=False
        )
    )

    recommendations = (
        serializers.ListField(
            required=False
        )
    )

    predictive_alerts = (
        serializers.ListField(
            required=False
        )
    )

    decisions = (
        serializers.DictField(
            required=False
        )
    )