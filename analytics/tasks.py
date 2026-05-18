from celery import shared_task
from django.utils import timezone

from data_ingestion.models import Dataset, DataRecord
from .models import FailedRow,AnalysisResult
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
    #clean previous processing
    DataRecord.objects.filter(dataset=dataset).delete()
    FailedRow.objects.filter(dataset=dataset).delete()
    
    #Reset counters
    dataset.processed_rows=0
    dataset.progress =0
    dataset.save(update_fields=["processed_rows","progress"])

 
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
        Dataset.objects.filter(id=dataset.id).update(
            status="failed"
            )
        FailedRow.objects.create(
            dataset=dataset,
            raw_data ="TASK_FAILURE",
            error=str(e)
        )

        raise e


@shared_task
def analyze_dataset_task(dataset_id):

    dataset = Dataset.objects.get(id=dataset_id)

    records = DataRecord.objects.filter(dataset=dataset)

    if not records.exists():
        return {"error": "No records found"}

    rows = [record.data for record in records]

    df = pd.DataFrame(rows)

    # ----------------------------
    # BASIC INFO
    # ----------------------------
    row_count = len(df)
    column_count = len(df.columns)

    numeric_df = df.apply(
        pd.to_numeric,
        errors="coerce"
    )

    numeric_df = numeric_df.dropna(
        axis=1,
        how="all"
    )


    # ----------------------------
    # STATISTICS
    # ----------------------------
    summary = {
        "dataset_info": {
            "rows": row_count,
            "columns": column_count,
            "numeric_columns": len(numeric_df.columns),
        },

        "statistics": {
            "mean": numeric_df.mean().to_dict(),
            "median": numeric_df.median().to_dict(),
            "max": numeric_df.max().to_dict(),
            "min": numeric_df.min().to_dict(),
            "sum": numeric_df.sum().to_dict(),
            "std_dev": numeric_df.std().to_dict(),
        },

        # ----------------------------
        # DATA QUALITY
        # ----------------------------
        "missing_values": (
            df.isnull()
            .sum()
            .to_dict()
        ),

        # ----------------------------
        # CATEGORY INSIGHTS
        # ----------------------------
        "top_record_types": (
            df["record_type"]
            .value_counts()
            .head(10)
            .to_dict()
            if "record_type" in df.columns
            else {}
        ),
    }

    # ----------------------------
    # DATA QUALITY SCORE
    # ----------------------------
    total_cells = df.shape[0] * df.shape[1]

    missing_cells = df.isnull().sum().sum()

    quality_score = round(
        (1 - (missing_cells / total_cells)) * 100,
        2
    )

    summary["quality_score"] = quality_score

    # ----------------------------
    # SIMPLE ANOMALY DETECTION
    # ----------------------------
    anomalies = {}

    for column in numeric_df.columns:

        mean = numeric_df[column].mean()
        std = numeric_df[column].std()

        if std == 0 or pd.isna(std):
            continue

        outliers = numeric_df[
            np.abs(numeric_df[column] - mean) > (3 * std)
        ]

        if not outliers.empty:
            anomalies[column] = len(outliers)

    summary["anomalies"] = anomalies

    # ----------------------------
    # SAVE RESULT
    # ----------------------------
    AnalysisResult.objects.update_or_create(
        dataset=dataset,
        defaults={
            "summary": summary
        }
    )

    return {
        "status": "analyzed",
        "quality_score": quality_score
    }