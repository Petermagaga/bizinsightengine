from django.db import models
from data_ingestion.models import Dataset

class AnalysisResult(models.Model):
    dataset=models.OneToOneField(
        Dataset, 
        on_delete=models.CASCADE,
        related_name="analysis"
    )
    summary=models.JSONField(default=dict)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Analysis for {self.dataset.name}"
    

class FailedRow(models.Model):
    dataset=models.ForeignKey(Dataset,
                              on_delete=models.CASCADE,
                              related_name="failed_rows"
                              )
    
    raw_data=models.TextField()
    error=models.TextField(
        null=True,
        blank=True
    )

    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Failed row for {self.dataset.name}"
    

    