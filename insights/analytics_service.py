import pandas as pd

def build_dataframe(dataset):
    records=[]

    for record in dataset.records.all():
        row=record.data.copy()
        row["sheet_name"]=(
            record.sheet_name
        )
        records.append(row)

    return pd.DataFrame(records)

def classify_question(question):

    question = question.lower()

    if "highest" in question:
        return "highest"

    if "lowest" in question:
        return "lowest"

    if "average" in question:
        return "average"

    if "mean" in question:
        return "average"

    if "total" in question:
        return "sum"

    if "sum" in question:
        return "sum"

    if "count" in question:
        return "count"

    return "ai"