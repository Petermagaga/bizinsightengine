import json
import pandas as pd
import numpy as np
import re

from groq import Groq
from django.conf import settings
from .forecast_service import generate_forecast

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
            "mean": round(float(values.mean()), 2),
            "max": round(float(values.max()), 2),
            "min": round(float(values.min()), 2),
            "sum": round(float(values.sum()), 2),
        }

    return {
        "total_rows": total_rows,
        "columns": columns,
        "sample_data": sample_data,
        "numeric_summary": numeric_summary,
    }

def build_ai_prompt(data_summary, anomalies, forecast_data):

    return f"""
You are an advanced AI business analyst.

Analyze the uploaded dataset, detected anomalies,
and forecast results.

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
  ],

  "anomaly_details": [
    {{
      "column": string,
      "value": string,
      "severity": string,
      "reason": string
    }}
  ]
}}

Dataset Summary:
{json.dumps(data_summary, indent=2)}

Detected Anomalies:
{json.dumps(anomalies, indent=2, default=str)}

Forecast Data:
{json.dumps(forecast_data, indent=2, default=str)}

Instructions:
- Use the anomaly data when calculating anomalies_found.
- Generate alerts from severe anomalies.
- Use forecast data when creating forecast_chart.
- Provide business recommendations based on both anomalies and forecasts.
- Return valid JSON only.
"""

def generate_dashboard_ai(records,anomalies,forecast_data):

    context = build_dataset_context(records)

    prompt = build_ai_prompt(context,anomalies,forecast_data)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior AI business analyst. "
                    "Return ONLY valid JSON. "
                    "Do not wrap the response in markdown code blocks."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    content = (
        response
        .choices[0]
        .message
        .content
    ).strip()

    try:

        # Remove markdown fences if present
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # Extract JSON object if model added extra text
        match = re.search(
            r"\{.*\}",
            content,
            re.DOTALL
        )

        if match:
            content = match.group(0)

        dashboard_data = json.loads(content)

        return dashboard_data

    except Exception as e:

        return {
            "kpis": {},
            "business_health": "Unknown",
            "summary": {
                "headline": "AI parsing failed",
                "key_takeaway": str(e)
            },
            "raw_response": content[:1000],
            "forecast_chart": [],
            "production_chart": [],
            "time_series": [],
            "alerts": [],
            "recommendations": [],
            "decisions": []
        }