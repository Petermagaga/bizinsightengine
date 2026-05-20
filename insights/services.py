from analytics.models import AnalysisResult
from .models import Insight
from .groq_service import generate_insight, build_prompt
from .forecasting import predict_next

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
    # Predictions (Smarter Version)
    # -----------------------------

    # -----------------------------
    # Predictions (Smarter Version)
    # -----------------------------
    predictions = {}

    try:
        print("New Prediction Logic Running")

        records = list(
            dataset.records
            .all()
            .values_list("data", flat=True)
        )

        print("Records:", len(records))

        import pandas as pd

        df = pd.DataFrame(records)

        print(df.head())

        numeric_df = df.select_dtypes(
            include=["number"]
        )

        print("Numeric columns:", numeric_df.columns)

        for column in numeric_df.columns:

            values = (
                numeric_df[column]
                .dropna()
                .tolist()
            )

            if len(values) < 3:
                continue

            recent_values = values[-5:]

            moving_average = round(
                sum(recent_values)
                / len(recent_values),
                2
            )

            first = recent_values[0]
            last = recent_values[-1]

            if last > first:
                trend = "increasing"

            elif last < first:
                trend = "decreasing"

            else:
                trend = "stable"

            predictions[column] = {
                "trend": trend,
                "predicted_next": max(
                    moving_average,
                    0
                )
            }

        print("Predictions created:", len(predictions))

    except Exception as e:
        print("PREDICTION ERROR:", str(e))

        predictions = {
            "error": str(e)
        }

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