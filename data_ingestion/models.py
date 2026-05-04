from django.db import models
from django.conf import settings

class Dataset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    file=models.FileField(upload_to="datasets/")
    progress=models.IntegerField(default=0)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(
        max_length=20,
        choices=[
            ('pending','Pending'),
            ('processing','Processing'),
            ('completed',"Completed"),
            ('failed','Failed'),
        ],
        default='pending'
    )
    total_rows=models.IntegerField(default=0)
    processed_rows = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class DataRecord(models.Model):
    dataset=models.ForeignKey(Dataset,on_delete=models.CASCADE,related_name="records")
    data=models.JSONField()

    def __str__(self):
        return f"Record {self.id} - {self.dataset.name}"

