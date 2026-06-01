import json
import re

import numpy as np
import pandas as pd
from groq import Groq
from django.conf import settings

client = Groq(
    api_key=settings.GROQ_API_KEY
)


# -----------------------------------
# JSON SERIALIZER
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


# -----------------------------------
# DATASET CONTEXT BUILDER
# -----------------------------------
def build_dataset_context(records):

    sheets = {}

    for record in records:

        sheet_name = record.get(
            "sheet_name",
            "Unknown"
        )

        row_data = record.get(
            "data",
            {}
        )

        sheets.setdefault(
            sheet_name,
            []
        ).append(row_data)

    sheet_summary = {}

    total_rows = 0

    for sheet_name, rows in sheets.items():

        df = pd.DataFrame(rows)

        total_rows += len(df)

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

            numeric_summary[
                str(column)
            ] = {
                "mean": round(
                    float(values.mean()),
                    2
                ),
                "max": round(
                    float(values.max()),
                    2
                ),
                "min": round(
                    float(values.min()),
                    2
                ),
                "sum": round(
                    float(values.sum()),
                    2
                ),
            }

        sample_data = (
            df.head(5)
            .replace({np.nan: None})
            .to_dict(
                orient="records"
            )
        )

        sheet_summary[
            sheet_name
        ] = {
            "row_count": len(df),
            "columns": [
                str(col)
                for col in df.columns
            ],
            "sample_data": sample_data,
            "numeric_summary": numeric_summary,
        }

    return {
        "sheet_count": len(sheets),
        "sheet_names": list(
            sheets.keys()
        ),
        "total_rows": total_rows,
        "sheets": sheet_summary,
    }


# -----------------------------------
# AI PROMPT
# -----------------------------------
def build_ai_prompt(
    data_summary,
    anomalies,
    forecast_data
):

    return f"""
You are an advanced AI business analyst.

Analyze the uploaded dataset,
detected anomalies,
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
{json.dumps(data_summary, indent=2, default=json_serializer)}

Detected Anomalies:
{json.dumps(anomalies, indent=2, default=json_serializer)}

Forecast Data:
{json.dumps(forecast_data, indent=2, default=json_serializer)}

MULTI-SHEET DATASET INFORMATION

The workbook may contain multiple sheets.

Each record follows:

{{
  "sheet_name": "Production",
  "data": {{
      "...": "row values"
  }}
}}

Analyze both:

1. Relationships within each sheet
2. Relationships across sheets

Look for:

- Production vs Inventory
- Production vs Maintenance
- Production vs Quality
- Inventory vs Sales
- Maintenance vs Downtime
- Quality vs Machine Performance
- Cross-sheet trends
- Operational bottlenecks
- Resource constraints
- Forecast risks

Examples:

- Production dropped after maintenance events.
- Inventory shortages correlate with reduced output.
- Quality issues increased after downtime.
- Maintenance activity improved quality metrics.
- Forecasted shortages may affect future production.

Instructions:

- Use anomaly data when calculating anomalies_found.
- Generate alerts from severe anomalies.
- Use forecast data when creating forecast_chart.
- Provide recommendations using anomalies and forecasts.
- When multiple sheets exist, generate cross-sheet insights whenever possible.
- Return ONLY valid JSON.
"""


# -----------------------------------
# GROQ DASHBOARD GENERATOR
# -----------------------------------
def generate_dashboard_ai(
    records,
    anomalies,
    forecast_data
):

    context = build_dataset_context(
        records
    )

    prompt = build_ai_prompt(
        context,
        anomalies,
        forecast_data
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior AI business analyst. "
                    "Return ONLY valid JSON. "
                    "Do not wrap responses in markdown. "
                    "Use cross-sheet analysis whenever possible."
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

        content = (
            content
            .replace(
                "```json",
                ""
            )
            .replace(
                "```",
                ""
            )
            .strip()
        )

        match = re.search(
            r"\{.*\}",
            content,
            re.DOTALL
        )

        if match:
            content = match.group(0)

        dashboard_data = json.loads(
            content
        )

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
            "time_series": [],
            "alerts": [],
            "recommendations": [],
            "decisions": [],
            "anomaly_details": []
        }