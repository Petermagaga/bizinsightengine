from django.db import models
from data_ingestion.models import Dataset

class AnalysisResult(models.Model):
    dataset=models.OneToOneField(Dataset,on_delete=models.CASCADE)
    summary=models.JSONField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" analysis for {self.dataset.name}"