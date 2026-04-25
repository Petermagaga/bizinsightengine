from celery import shared_task
from data_ingestion.models import Dataset
from .services import compute_basic_statistics
from insights.services import generate_insights_for_dataset

@shared_task
def process_dataset_task(dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id)
    except Dataset.DoesNotExist:
        return "Dataset not found"

    # run analysis
    compute_basic_statistics(dataset)

    # generate AI insights
    generate_insights_for_dataset(dataset)

    return f"Processing completed for dataset {dataset_id}"
