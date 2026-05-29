import json
import pandas as pd

from groq import Groq
from django.conf import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


# -----------------------------------
# DATASET SUMMARIZER
# -----------------------------------

def build_dataset_context(records):

    df = pd.DataFrame(records)

    total_rows = len(df)

    columns = list(df.columns)

    sample_data = (
        df.head(10)
        .fillna("")
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

        numeric_summary[column] = {
            "mean": round(values.mean(), 2),
            "max": round(values.max(), 2),
            "min": round(values.min(), 2),
            "sum": round(values.sum(), 2),
        }

    return {
        "total_rows": total_rows,
        "columns": columns,
        "sample_data": sample_data,
        "numeric_summary": numeric_summary,
    }


# -----------------------------------
# PROMPT BUILDER
# -----------------------------------

def build_ai_prompt(context):

    return f"""
You are an advanced AI business intelligence system.

Analyze this uploaded business dataset.

Generate REAL business insights.

Return ONLY valid JSON.

Required JSON structure:

{{
  "kpis": {{
      "top_metric": "",
      "top_value": 0,
      "quality_score": 0,
      "anomalies_found": 0
  }},

  "business_health": "",

  "summary": {{
      "headline": "",
      "key_takeaway": ""
  }},

  "forecast_chart": [],

  "production_chart": [],

  "time_series": [],

  "alerts": [],

  "recommendations": [],

  "decisions": []
}}

Rules:
- Return ONLY JSON
- No markdown
- No explanation
- No code blocks
- Make realistic business conclusions
- Detect trends
- Detect risks
- Generate KPI insights
- Generate recommendations
- Generate operational decisions
- Generate chart-ready arrays

Dataset Context:
{json.dumps(context)}
"""


# -----------------------------------
# MAIN AI ENGINE
# -----------------------------------

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