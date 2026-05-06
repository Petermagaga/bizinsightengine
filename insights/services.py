# insights/services.py

from analytics.models import AnalysisResult
from .models import Insight
from .groq_service import generate_insight, build_prompt
import pandas as pd

def generate_insights_for_dataset(dataset):
    try:
        analysis = AnalysisResult.objects.get(dataset=dataset)
    except AnalysisResult.DoesNotExist:
        return {"error": "No analysis found"}

    summary_data = analysis.summary

    # -------------------------
    # Tier 1: Simple AI summary
    # -------------------------
    prompt = build_prompt(summary_data)
    ai_text = generate_insight(prompt).strip()

    if not ai_text:
        ai_text = "No insights generated."

    # -------------------------
    # Tier 2: BI logic (Python first)
    # -------------------------
    bi_insights = {}

    try:
        numeric_cols = summary_data.get("mean", {})

        if numeric_cols:
            top_metric = max(numeric_cols, key=numeric_cols.get)
            bi_insights["top_metric"] = top_metric

    except Exception:
        pass

    # -------------------------
    # Tier 3: Simple prediction
    # -------------------------
    predictions = {}

    try:
        if "mean" in summary_data:
            values = list(summary_data["mean"].values())
            if values:
                avg = sum(values) / len(values)
                predictions["next_estimate"] = avg * 1.1  # simple growth assumption
    except Exception:
        pass

    # -------------------------
    # Save everything
    # -------------------------
    insight = Insight.objects.create(
        dataset=dataset,
        summary_text=ai_text,
        bi_insights=bi_insights,
        predictions=predictions
    )

    return insight.id