from analytics.models import AnalysisResult
from .models import Insight
from .groq_service import generate_insight, build_prompt

def generate_insights_for_dataset(dataset):
    try:
        analysis = AnalysisResult.objects.get(dataset=dataset)
    except AnalysisResult.DoesNotExist:
        return {"error": "No analysis found for this dataset"}

    
    prompt = build_prompt(analysis.summary)

    ai_response = generate_insight(prompt)

    if not ai_response:
        ai_response = "No insights generated."

    insight = Insight.objects.create(
        dataset=dataset,
        contents=ai_response
    )

    return insight