from celery import shared_task
from data_ingestion.models import Dataset
from analytics.models import AnalysisResult
from .services import compute_basic_statistics
from insights.services import generate_insights_for_dataset

@shared_task
def process_dataset_task(dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id)
    except Dataset.DoesNotExist:
        return "Dataset not found"

    if AnalysisResult.objects.filter(dataset=dataset).exists():
        return f"Dataset {dataset_id} already processed"

    compute_basic_statistics(dataset)
    generate_insights_for_dataset(dataset)

    return f"Processing completed for dataset {dataset_id}"