from celery import shared_task
from django.utils import timezone
from django.db import transaction

from data_ingestion.models import Dataset, DataRecord
from .models import FailedRow, CleanDataRecord,AnalysisResult
from data_ingestion.utils.parse_excel import parse_excel

import pandas as pd
import numpy as np


def clean_row(row):
    """
    Convert all values into JSON-safe native Python types.
    Handles:
    - NaN / NaT
    - numpy integers/floats
    - pandas timestamps
    - normal Python values
    """

    cleaned = {}

    for key, value in row.items():

        # Handle NaN / NaT
        if pd.isna(value):
            cleaned[key] = None

        # Convert numpy integers
        elif isinstance(value, (np.integer,)):
            cleaned[key] = int(value)

        # Convert numpy floats
        elif isinstance(value, (np.floating,)):
            cleaned[key] = float(value)

        # Convert pandas timestamps
        elif isinstance(value, pd.Timestamp):
            cleaned[key] = value.isoformat()

        # Keep JSON-safe native values
        elif isinstance(value, (int, float, str, bool, list, dict)):
            cleaned[key] = value

        # Fallback conversion
        else:
            cleaned[key] = str(value)

    return cleaned


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3}
)
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

        dataset.save(
            update_fields=["status", "progress", "started_at"]
            if hasattr(dataset, "started_at")
            else ["status", "progress"]
        )

        buffer = []
        processed = 0

        # STEP 2: stream + process
        for row in parse_excel(dataset.file):

            try:
                cleaned_row = clean_row(row)

                buffer.append(
                    DataRecord(
                        dataset=dataset,
                        data=cleaned_row
                    )
                )

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

            # STEP 4: lightweight progress update
            if processed % PROGRESS_UPDATE_EVERY == 0:
                Dataset.objects.filter(id=dataset.id).update(
                    processed_rows=processed
                )

        # FINAL FLUSH
        if buffer:
            DataRecord.objects.bulk_create(buffer)

        # FINAL UPDATE
        update_data = {
            "status": "completed",
            "progress": 100,
            "processed_rows": processed,
        }

        if hasattr(dataset, "completed_at"):
            update_data["completed_at"] = timezone.now()

        Dataset.objects.filter(id=dataset.id).update(**update_data)

        return {
            "dataset_id": dataset.id,
            "rows_processed": processed
        }

    except Exception as e:
        Dataset.objects.filter(id=dataset.id).update(status="failed")
        raise e


@shared_task
def transform_dataset_task(dataset_id):

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

@shared_task
def analyze_dataset_task(dataset_id):

    dataset = Dataset.objects.get(id=dataset_id)

    records = CleanDataRecord.objects.filter(dataset=dataset)

    if not records.exists():
        return {"error": "No clean records found"}

    # convert to dataframe
    data = []

    for record in records:
        data.append({
            "column_1": record.column_1,
        })

    df = pd.DataFrame(data)

    summary = {
        "mean": df.mean(numeric_only=True).to_dict(),
        "max": df.max(numeric_only=True).to_dict(),
        "min": df.min(numeric_only=True).to_dict(),
        "count": int(len(df)),
    }

    AnalysisResult.objects.create(
        dataset=dataset,
        summary=summary
    )

    return {"status": "analyzed"}