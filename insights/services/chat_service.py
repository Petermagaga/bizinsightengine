import time

from groq import Groq
from django.conf import settings
from .analytics_service import (try_analytics_answer)
from .context_builder import (
    build_chat_context
)

from .prompt_builder import (
    build_chat_prompt
)

from insights.models import DatasetChat

client = Groq(
    api_key=settings.GROQ_API_KEY
)

def ask_dataset_question(
    dataset,
    question
):
    
    analytics_answer = (
        try_analytics_answer(
            dataset,
            question
        )
    )

    if analytics_answer:

        DatasetChat.objects.create(
            dataset=dataset,
            question=question,
            answer=analytics_answer,
            response_source="analytics"
        )

        return {
            "answer":
                analytics_answer,

            "source":
                "analytics"
        }



    start_time = time.time()

    context = build_chat_context(
        dataset
    )

    prompt = build_chat_prompt(
        context,
        question
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    answer = (
        response
        .choices[0]
        .message
        .content
    )

    DatasetChat.objects.create(
        dataset=dataset,
        question=question,
        answer=answer,
        response_source="ai",
        response_time=(
            time.time() - start_time
        )
    )

    return answer