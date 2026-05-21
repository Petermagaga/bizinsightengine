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



class DashboardSerializer:

    @staticmethod
    def build(dataset):

        return {
            "dataset_id":
                dataset.id,

            "generated_at":
                dataset.created_at,

            "kpis":
                dataset.kpis or {},

            "production_chart":
                dataset.production_chart or [],

            "forecast_chart":
                dataset.forecast_chart or [],

            "time_series":
                dataset.time_series or [],

            "trend_summary":
                dataset.trend_summary or {},

            "business_health":
                dataset.business_health,

            "summary":
                dataset.summary or {},

            "alerts":
                dataset.alerts or [],

            "recommendations":
                dataset.recommendations or [],

            "predictive_alerts":
                dataset.predictive_alerts or [],

            "decisions":
                dataset.decisions or {}
        }