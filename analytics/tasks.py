from celery import shared_task
from django.utils import timezone
from django.db import transaction

from data_ingestion.models import Dataset, DataRecord
from .models import FailedRow,CleanDataRecord
from data_ingestion.utils.parse_excel import parse_excel


def clean_row(row):
    """
    Ensure JSON-safe values.
    """
    from datetime import datetime, date

    cleaned = {}
    for k, v in row.items():
        if isinstance(v, (datetime, date)):
            cleaned[k] = v.isoformat()
        elif v is None:
            cleaned[k] = None
        elif isinstance(v, (int, float, str, bool)):
            cleaned[k] = v
        else:
            cleaned[k] = str(v)

    return cleaned


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def process_dataset_task(self, dataset_id):
    """
    Production-ready dataset processor:
    - Streams Excel (memory safe)
    - Cleans data
    - Bulk inserts (fast)
    - Tracks progress efficiently
    - Logs failed rows
    """

    dataset = Dataset.objects.get(id=dataset_id)

    # CONFIG
    BATCH_SIZE = 500
    PROGRESS_UPDATE_EVERY = 200

    try:
        # STEP 1: mark as processing
        dataset.status = "processing"
        dataset.progress = 0
        if hasattr(dataset, "started_at"):
            dataset.started_at = timezone.now()
        dataset.save(update_fields=["status", "progress", "started_at"] if hasattr(dataset, "started_at") else ["status", "progress"])

        buffer = []
        processed = 0

        # STEP 2: stream + process
        for row in parse_excel(dataset.file):  # generator (memory safe)
            try:
                cleaned = clean_row(row)

                buffer.append(DataRecord(
                    dataset=dataset,
                    data=cleaned
                ))

            except Exception as e:
                FailedRow.objects.create(
                    dataset=dataset,
                    raw_data=str(row),
                    error=str(e)
                )
            processed += 1

            # STEP 3: bulk insert
            if len(buffer) >= BATCH_SIZE:
                DataRecord.objects.bulk_create(buffer)
                buffer = []

            # STEP 4: progress update (lightweight)
            if processed % PROGRESS_UPDATE_EVERY == 0:
                Dataset.objects.filter(id=dataset.id).update(
                    processed_rows=processed
                )

        # FINAL FLUSH
        if buffer:
            DataRecord.objects.bulk_create(buffer)

        # FINAL UPDATE
        Dataset.objects.filter(id=dataset.id).update(
            status="completed",
            progress=100,
            processed_rows=processed,
            completed_at=timezone.now() if hasattr(dataset, "completed_at") else None
        )

        return {
            "dataset_id": dataset.id,
            "rows_processed": processed
        }

    except Exception as e:
        Dataset.objects.filter(id=dataset.id).update(status="failed")
        raise e

@shared_task
def transform_dataset_task(previous_result, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)

    records = DataRecord.objects.filter(dataset=dataset).iterator()

    clean_buffer = []
    BATCH_SIZE = 500

    for record in records:
        data = record.data

        try:
            clean_buffer.append(
                CleanDataRecord(
                    dataset=dataset,
                    column_1=float(data.get("amount", 0) or 0),
                    column_2=data.get("name")
                )
            )

        except Exception as e:
            # optional: log transform errors
            FailedRow.objects.create(
                dataset=dataset,
                raw_data=str(data),
                error=f"Transform error: {str(e)}"
            )

        if len(clean_buffer) >= BATCH_SIZE:
            CleanDataRecord.objects.bulk_create(clean_buffer)
            clean_buffer = []

    if clean_buffer:
        CleanDataRecord.objects.bulk_create(clean_buffer)

    return {"status": "transformed"}