import json
import pandas as pd
import numpy as np
from groq import Groq
from django.conf import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


# -----------------------------------
# DATASET SUMMARIZER
# -----------------------------------
def json_serializer(obj):

    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.bool_):
        return bool(obj)

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()

    if pd.isna(obj):
        return None

    return str(obj)

def build_dataset_context(records):

    df = pd.DataFrame(records)

    total_rows = int(len(df))

    columns = [str(col) for col in df.columns]

    # Convert dataframe rows safely
    sample_data = (
        df.head(10)
        .replace({np.nan: None})
        .to_dict(orient="records")
    )

    numeric_summary = {}

    numeric_df = df.select_dtypes(
        include=["number"]
    )

    for column in numeric_df.columns:

        values = (
            pd.to_numeric(
                numeric_df[column],
                errors="coerce"
            )
            .dropna()
        )

        if len(values) == 0:
            continue

        numeric_summary[str(column)] = {

            "mean": float(
                round(float(values.mean()), 2)
            ),

            "max": float(
                round(float(values.max()), 2)
            ),

            "min": float(
                round(float(values.min()), 2)
            ),

            "sum": float(
                round(float(values.sum()), 2)
            ),
        }

    return {
        "total_rows": int(total_rows),
        "columns": columns,
        "sample_data": sample_data,
        "numeric_summary": numeric_summary,
    }


# -----------------------------------
# PROMPT BUILDER
# -----------------------------------

import json


def build_ai_prompt(data_summary):

    return f"""
You are an advanced AI business analyst.

Analyze the uploaded dataset and generate
a COMPLETE dashboard JSON response.

Return ONLY valid JSON.

Required JSON structure:

{{
  "kpis": {{
    "quality_score": number,
    "top_metric": string,
    "top_value": number,
    "anomalies_found": number,
    "forecast_count": number
  }},

  "summary": {{
    "headline": string,
    "key_takeaway": string
  }},

  "business_health": string,

  "alerts": [
    {{
      "level": string,
      "message": string
    }}
  ],

  "recommendations": [
    {{
      "priority": string,
      "title": string,
      "message": string
    }}
  ],

  "forecast_chart": [
    {{
      "label": string,
      "prediction": number,
      "trend": string
    }}
  ],

  "time_series": [
    {{
      "date": string,
      "production": number
    }}
  ],

  "decisions": [
    {{
      "action": string,
      "priority": string,
      "recommendation": string
    }}
  ]
}}

Dataset Summary:
{json.dumps(data_summary, indent=2)}

Return JSON ONLY.
"""

def generate_dashboard_ai(records):

    context = build_dataset_context(
        records
    )

    prompt = build_ai_prompt(
        context
    )

    response = (
        client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content":
                    (
                        "You are a senior "
                        "AI business analyst."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
        )
    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    try:

        dashboard_data = json.loads(
            content
        )

        return dashboard_data

    except Exception:

        return {
            "kpis": {},
            "business_health":
                "Unknown",

            "summary": {
                "headline":
                    "AI parsing failed",

                "key_takeaway":
                    content[:300]
            },

            "forecast_chart": [],
            "production_chart": [],
            "time_series": [],
            "alerts": [],
            "recommendations": [],
            "decisions": []
        }