import json
import time
from .anomaly_detection import(detect_anomalies)
import pandas as pd
from .models import Insight
from .groq_service import (
    generate_dashboard_ai,
)

from data_ingestion.models import Dataset


def generate_insights_for_dataset(dataset):

    start_time = time.time()

    records = list(
        dataset.records.all()
        .values_list("data", flat=True)
    )

    if not records:
        raise Exception("No dataset records found")


    df = pd.DataFrame(records)

    anomalies = detect_anomalies(records)

    print("Detected anomalies:")
    print(anomalies)


    dashboard_data = generate_dashboard_ai(records,anomalies)

    Insight.objects.filter(
        dataset=dataset
    ).delete()

    processing_time = (
        time.time() - start_time
    )

    insight = Insight.objects.create(
        dataset=dataset,
        dashboard_data=dashboard_data,
        raw_ai_response=json.dumps(
            dashboard_data,
            default=str
        ),
        ai_model="llama-3.1-8b-instant",
        processing_time=processing_time
    )

    return insight.id