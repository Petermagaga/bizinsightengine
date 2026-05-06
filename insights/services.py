from analytics.models import AnalysisResult
from .models import Insight
from .groq_service import generate_insight, build_prompt


def generate_insights_for_dataset(dataset):
    """
    Generate AI + BI + prediction insights for a dataset.
    Safe, cached, and production-ready.
    """

    # -----------------------------------
    # 0. Prevent duplicate generation
    # -----------------------------------
    existing = Insight.objects.filter(dataset=dataset).first()
    if existing:
        return existing.id

    # -----------------------------------
    # 1. Get analysis data
    # -----------------------------------
    try:
        analysis = AnalysisResult.objects.get(dataset=dataset)
    except AnalysisResult.DoesNotExist:
        return {"error": "No analysis found"}

    summary_data = analysis.summary or {}

    # -----------------------------------
    # 2. AI Insight (safe call)
    # -----------------------------------
    try:
        prompt = build_prompt(summary_data)
        ai_text = generate_insight(prompt).strip()
    except Exception:
        ai_text = "AI insight generation failed."

    if not ai_text:
        ai_text = "No insights generated."

    # -----------------------------------
    # 3. BI Insights (stronger logic)
    # -----------------------------------
    bi_insights = {}

    try:
        numeric_cols = summary_data.get("mean", {})

        if numeric_cols:
            top_metric = max(numeric_cols, key=numeric_cols.get)
            lowest_metric = min(numeric_cols, key=numeric_cols.get)
            avg_value = sum(numeric_cols.values()) / len(numeric_cols)

            bi_insights = {
                "top_metric": top_metric,
                "lowest_metric": lowest_metric,
                "average_value": avg_value
            }

    except Exception:
        bi_insights = {}

    # -----------------------------------
    # 4. Predictions (improved logic)
    # -----------------------------------
    predictions = {}

    try:
        values = list(summary_data.get("mean", {}).values())

        if values:
            trend = 0
            if len(values) > 1:
                trend = values[-1] - values[0]

            predictions = {
                "trend": "increasing" if trend > 0 else "decreasing",
                "next_estimate": values[-1] + trend if values else None
            }

    except Exception:
        predictions = {}

    # -----------------------------------
    # 5. Save insight
    # -----------------------------------
    insight = Insight.objects.create(
        dataset=dataset,
        summary_text=ai_text,
        bi_insights=bi_insights,
        predictions=predictions
    )

    return insight.id