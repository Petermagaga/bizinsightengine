# insights/tasks.py

from celery import shared_task
from data_ingestion.models import Dataset
from .services import generate_insights_for_dataset


@shared_task
def generate_insight_task(previous_result,dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)
    return generate_insights_for_dataset(dataset)