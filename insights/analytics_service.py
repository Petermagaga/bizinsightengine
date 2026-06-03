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

def answer_highest(df):

    numeric_cols = (
        df.select_dtypes(
            include=["number"]
        ).columns
    )

    if len(numeric_cols) == 0:

        return None

    col = numeric_cols[0]

    row = df.loc[
        df[col].idxmax()
    ]

    return (
        f"Highest {col} is "
        f"{row[col]}"
    )

def answer_lowest(df):

    numeric_cols = (
        df.select_dtypes(
            include=["number"]
        ).columns
    )

    if len(numeric_cols) == 0:

        return None

    col = numeric_cols[0]

    row = df.loc[
        df[col].idxmin()
    ]

    return (
        f"Lowest {col} is "
        f"{row[col]}"
    )

def answer_count(df):

    return (
        f"The dataset contains "
        f"{len(df)} records."
    )

def answer_average(df):

    numeric_cols = (
        df.select_dtypes(
            include=["number"]
        ).columns
    )

    if len(numeric_cols) == 0:
        return None

    col = numeric_cols[0]

    return (
        f"Average {col} is "
        f"{round(df[col].mean(),2)}"
    )
def try_analytics_answer(
    dataset,
    question
):

    df = build_dataframe(
        dataset
    )

    intent = classify_question(
        question
    )

    if intent == "highest":
        return answer_highest(df)

    if intent == "lowest":
        return answer_lowest(df)

    if intent == "average":
        return answer_average(df)

    if intent == "count":
        return answer_count(df)

    return None