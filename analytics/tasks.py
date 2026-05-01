# analytics/tasks.py

from celery import shared_task
from django.db import transaction

from data_ingestion.models import Dataset, DataRecord
from data_ingestion.utils import parse_excel
from utils.data_cleaning import clean_row

from analytics.services import compute_basic_statistics
from insights.services import generate_insights_for_dataset


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_dataset_task(self, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id)
    except Dataset.DoesNotExist:
        return f"Dataset {dataset_id} not found"

    try:
        with transaction.atomic():

            # 1. Parse Excel
            parsed_data = parse_excel(dataset.file)

            if not parsed_data:
                return f"No data found in dataset {dataset_id}"

            # 2. Clean + prepare records
            records = []
            for row in parsed_data:
                clean_data = clean_row(row)
                records.append(DataRecord(dataset=dataset, data=clean_data))

            # 3. Bulk insert
            DataRecord.objects.bulk_create(records)

            # 4. Compute analytics
            compute_basic_statistics(dataset)

            # 5. Generate insights
            generate_insights_for_dataset(dataset)

    except Exception as e:
        # Optional: log error in DB or monitoring system
        raise self.retry(exc=e)

    return f"Dataset {dataset_id} processed successfully"