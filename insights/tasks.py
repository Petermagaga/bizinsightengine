from celery import shared_task
from django.utils import timezone

from data_ingestion.models import (
    Dataset,
    DataRecord
)

from data_ingestion.utils.parse_excel import (
    parse_excel
)

from data_ingestion.utils.data_cleaning import (
    clean_row
)

from .services import (
    generate_insights_for_dataset
)


@shared_task
def process_dataset_task(dataset_id):

    dataset = Dataset.objects.get(id=dataset_id)

    try:

        dataset.status = "processing"
        dataset.progress = 10
        dataset.save()

        records = parse_excel(
            dataset.file.path
        )

        dataset.total_rows = len(records)
        dataset.save()

        cleaned_records = []

        for index, row in enumerate(records):

            cleaned = clean_row(row)

            cleaned_records.append(
                DataRecord(
                    dataset=dataset,
                    data=cleaned
                )
            )

            progress = int(
                ((index + 1) / len(records)) * 50
            )

            dataset.progress = progress
            dataset.processed_rows = index + 1
            dataset.save()

        DataRecord.objects.bulk_create(
            cleaned_records
        )

        dataset.progress = 60
        dataset.save()

        return dataset.id

    except Exception as e:

        dataset.status = "failed"
        dataset.save()

        raise e


@shared_task
def generate_insight_task(dataset_id):

    dataset = Dataset.objects.get(id=dataset_id)

    try:

        dataset.progress = 70
        dataset.save()

        generate_insights_for_dataset(
            dataset
        )

        dataset.progress = 100
        dataset.status = "completed"
        dataset.completed_at = timezone.now()
        dataset.save()

        return {
            "status": "completed"
        }

    except Exception as e:

        dataset.status = "failed"
        dataset.save()

        raise e