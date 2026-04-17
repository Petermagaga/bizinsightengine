from analytics.models import AnalysisResult
from .models import Insight
from .groq_service import generate_insight, build_prompt

def generate_insights_for_dataset(dataset):
    try:
        analysis = AnalysisResult.objects.get(dataset=dataset)
    except AnalysisResult.DoesNotExist:
        return {"error": "No analysis found for this dataset"}

    
    prompt = build_prompt(analysis.summary)

    ai_response = generate_insight(prompt).strip()

    if not ai_response:
        ai_response = "No insights generated."

    insight = Insight.objects.create(
        dataset=dataset,
        contents=ai_response
    )

    return insight



from data_ingestion.models import Dataset
from insights.services import generate_insights_for_dataset

dataset = Dataset.objects.first()
insight = generate_insights_for_dataset(dataset)

print(insight.contents)