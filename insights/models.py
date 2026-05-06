from django.db import models
from data_ingestion.models import Dataset


class Insight(models.Model):
    dataset=models.ForeignKey(Dataset,on_delete=models.CASCADE)
    summary_text=models.TextField()
    bi_insights=models.JSONField(null=True)
    predictions=models.JSONField(null=True)
    
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Insight for {self.dataset.name} at {self.created_at} "



