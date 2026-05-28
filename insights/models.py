from django.db import models
from data_ingestion.models import Dataset

class Insight(models.Model):

    dataset=models.ForeignKey(Dataset,on_delete=models.CASCADE,related_name="insights")
    dashboard_data=models.JSONField(
        default=dict, blank=True
    )
    raw_ai_response=models.TextField(
        blank=True,null=True
    )
    ai_model=models.CharField(
        max_length=100,default="groq"
    )
    processing_time=models.FloatField(
        null=True,blank=True
    )
    created_at=models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        ordering=["-created_at"]
    def __str__(self):
        return (
            f"Insight for "
            f"{self.dataset.name}"
        )
