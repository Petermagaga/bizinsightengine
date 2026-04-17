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
You are a business analyst.

Analyze the following business data summary and provide:

1. Key insights
2. Notable trends
3. Business risks (if any)
4. Actionable recommendations

Data Summary:
{summary}

Respond clearly in plain English.
"""

