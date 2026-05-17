from groq import Groq
from django.conf import settings

client= Groq(api_key=settings.GROQ_API_KEY)

def generate_insight(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role":"system","content":"You are a business analyst AI"},
            {"role":"user","content":prompt}
        ]
    )
    return response.choices[0].message.content


def build_prompt(summary):
    return f"""
You are a senior business intelligence analyst.

Analyze the dataset and provide:

1. Executive Summary
2. Key business insights
3. Production or operational trends
4. Risks or anomalies
5. Data quality observations
6. Actionable recommendations

Rules:
- Be specific.
- Use numbers where relevant.
- Mention unusual patterns.
- Mention operational risks.
- Keep it professional and concise.

Dataset Analysis:
{summary}

Return clear business insights in plain English.
"""