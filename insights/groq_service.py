from groq import Groq
from django.conf import settings

client= Groq(api_key=settings.GROQ_API_KEY)

def generate_insight(prompt):
    response = client.chat.completions.create(
        model ="llama3-70b-8192",
        messages=[
            {"role":"system","content":"You are a business analyst AI"},
            {"role":"user","content":prompt}
        ]
    )