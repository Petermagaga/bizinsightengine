from django.db import models
from data_ingestion.models import Dataset


class Insight(models.Model):

    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name="insights"
    )

    # Human-readable AI summary
    summary_text = models.TextField(
        blank=True,
        null=True
    )

    # Business intelligence insights
    bi_insights = models.JSONField(
        default=dict,
        blank=True
    )

    # ML / forecasting / predictions
    predictions = models.JSONField(
        default=dict,
        blank=True
    )

    # Dashboard-ready charts/cards/tables
    dashboard_data = models.JSONField(
        default=dict,
        blank=True
    )

    # Raw full AI output (for debugging/auditing)
    raw_ai_response = models.TextField(
        blank=True,
        null=True
    )

    # Which AI provider/model generated this
    ai_model = models.CharField(
        max_length=100,
        default="groq"
    )

    # Time taken for processing
    processing_time = models.FloatField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Insight for {self.dataset.name}"
    
class DatasetChat(models.Model):
    Dataset=models.ForeignKey(Dataset,on_delete=models.CASCADE, related_name="chats")
    question=models.TextField()
    answer=models.TextField()
    response_source=models.CharField(
        max_length=20,default="ai"
    )
    response_time=models.FloatField(
        null=True,
        blank=True
    )
    created_at=models.DateTimeField(
        auto_now_add=True
    )