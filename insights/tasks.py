from celery import shared_task
from data_ingestion.models import Dataset
from .services import generate_ai_dashboard


@shared_task
def generate_insight_task(dataset_id):

    try:

        dataset = Dataset.objects.get(
            id=dataset_id
        )

        return generate_ai_dashboard(
            dataset
        )

    except Dataset.DoesNotExist:

        return {
            "error":
            "Dataset not found"
        }

    except Exception as e:

        return {
            "error": str(e)
        }

