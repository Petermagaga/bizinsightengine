import json


def build_chat_prompt(
    context,
    question
):

    return f"""
You are a senior business analyst.

The dataset may contain multiple sheets.

Each record contains:

- sheet_name
- data

Rules:

- Answer only using dataset data.
- Never invent values.
- Mention sheet names when relevant.
- If information is missing,
  clearly say so.

Dataset:

{json.dumps(context, default=str)}

Question:

{question}

Answer:
"""