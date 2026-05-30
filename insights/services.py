import json
import time

from .models import Insight
from .groq_service import (
    generate_dashboard_ai,
    build_ai_prompt
)

from data_ingestion.models import Dataset


def generate_insights_for_dataset(dataset):

    start_time = time.time()

    records = list(
        dataset.records
        .all()
        .values_list("data", flat=True)
    )

    if not records:

        raise Exception(
            "No dataset records found"
        )

    sample_data = records[:20]

    prompt = build_ai_prompt(sample_data)

    ai_response = generate_dashboard_ai(prompt)

    try:

        dashboard_data = json.loads(
            ai_response
        )

    except Exception:

        dashboard_data = {
            "summary": {
                "headline":
                    "AI response parsing failed",

                "key_takeaway":
                    ai_response
            }
        }

    Insight.objects.filter(
        dataset=dataset
    ).delete()

    processing_time = (
        time.time() - start_time
    )

    insight = Insight.objects.create(
        dataset=dataset,
        dashboard_data=dashboard_data,
        raw_ai_response=ai_response,
        ai_model="llama-3.1-8b-instant",
        processing_time=processing_time
    )

    return insight.id