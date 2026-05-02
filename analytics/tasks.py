# analytics/tasks.py

from celery import shared_task
from django.db import transaction

from data_ingestion.models import Dataset, DataRecord
from data_ingestion.utils.parse_excel import parse_excel
from data_ingestion.utils.data_cleaning import clean_row

from analytics.services import compute_basic_statistics
from insights.services import generate_insights_for_dataset


@shared_task(bind=True)
def process_dataset_task(self, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)

    try:
        dataset.status = "processing"
        dataset.progress = 10
        dataset.save(update_fields=["status", "progress"])

        parsed_data = parse_excel(dataset.file)

        dataset.progress = 30
        dataset.save(update_fields=["progress"])

        records = []
        for row in parsed_data:
            records.append(DataRecord(dataset=dataset, data=clean_row(row)))

        DataRecord.objects.bulk_create(records)

        dataset.progress = 60
        dataset.save(update_fields=["progress"])

        compute_basic_statistics(dataset)

        dataset.progress = 80
        dataset.save(update_fields=["progress"])

        generate_insights_for_dataset(dataset)

        dataset.status = "completed"
        dataset.progress = 100
        dataset.save(update_fields=["status", "progress"])

    except Exception as e:
        dataset.status = "failed"
        dataset.save(update_fields=["status"])
        raise e
    
    return f"Dataset {dataset_id} processed successfully"