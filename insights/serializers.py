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
    def build(insight):

        return {
            "dataset_id":
                insight.dataset.id,

            "generated_at":
                insight.created_at,

            "kpis":
                insight.kpis or {},

            "production_chart":
                insight.production_chart or [],

            "forecast_chart":
                insight.forecast_chart or [],

            "time_series":
                insight.time_series or [],

            "trend_summary":
                insight.trend_summary or {},

            "business_health":
                insight.business_health,

            "summary":
                insight.summary or {},

            "alerts":
                insight.alerts or [],

            "recommendations":
                insight.recommendations or [],

            "predictive_alerts":
                insight.predictive_alerts or [],

            "decisions":
                insight.decisions or {}
        }