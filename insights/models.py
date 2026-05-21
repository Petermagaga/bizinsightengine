from django.db import models
from data_ingestion.models import Dataset

class Meta: 
    ordering=["-created_at "]
    
class Insight(models.Model):

    dataset=models.ForeignKey(Dataset,on_delete=models.CASCADE)
    summary_text=models.TextField(null=True,blank=True)
    bi_insights=models.JSONField(default=dict,blank=True)
    predictions=models.JSONField(default=dict,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Insight for {self.dataset.name} at {self.created_at} "



