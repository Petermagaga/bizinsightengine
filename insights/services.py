from analytics.models import AnalysisResult
from .models import Insight
from .groq_service import generate_insight, build_prompt


def generate_insights_for_dataset(dataset):
    """
    Generate AI + BI + prediction insights.
    """

    # -----------------------------
    # Prevent duplicate generation
    # -----------------------------
    existing = Insight.objects.filter(
        dataset=dataset
    ).first()

    if existing:
        existing.delete()

    # -----------------------------
    # Get analysis
    # -----------------------------
    try:
        analysis = AnalysisResult.objects.get(
            dataset=dataset
        )
    except AnalysisResult.DoesNotExist:
        return {"error": "No analysis found"}

    summary_data = analysis.summary or {}

    statistics = summary_data.get(
        "statistics", {}
    )

    mean_stats = statistics.get(
        "mean", {}
    )

    # -----------------------------
    # AI Insight
    # -----------------------------
    try:
        prompt = build_prompt(summary_data)

        ai_text = generate_insight(
            prompt
        ).strip()

    except Exception as e:
        ai_text = (
            f"AI insight generation failed: {str(e)}"
        )

    if not ai_text:
        ai_text = "No insights generated."

    # -----------------------------
    # BI Insights
    # -----------------------------
    bi_insights = {}

    try:

        if mean_stats:

            top_metric = max(
                mean_stats,
                key=mean_stats.get
            )

            lowest_metric = min(
                mean_stats,
                key=mean_stats.get
            )

            avg_value = round(
                sum(mean_stats.values())
                / len(mean_stats),
                2
            )

            bi_insights = {
                "top_metric": top_metric,
                "top_value":
                    mean_stats[top_metric],

                "lowest_metric":
                    lowest_metric,

                "lowest_value":
                    mean_stats[lowest_metric],

                "overall_average":
                    avg_value,

                "quality_score":
                    summary_data.get(
                        "quality_score"
                    ),

                "anomalies_found":
                    len(
                        summary_data.get(
                            "anomalies", {}
                        )
                    )
            }

    except Exception:
        bi_insights = {}

    # -----------------------------
    # Predictions
    # -----------------------------
    predictions = {}

    try:

        values = list(
            mean_stats.values()
        )

        if len(values) > 1:

            trend_value = (
                values[-1]
                - values[0]
            )

            predictions = {
                "trend":
                    (
                        "increasing"
                        if trend_value > 0
                        else "decreasing"
                    ),

                "confidence":
                    "low",

                "estimated_next":
                    round(
                        values[-1]
                        + trend_value,
                        2
                    )
            }

    except Exception:
        predictions = {}

    # -----------------------------
    # Save insight
    # -----------------------------
    insight = Insight.objects.create(
        dataset=dataset,
        summary_text=ai_text,
        bi_insights=bi_insights,
        predictions=predictions
    )

    return insight.id