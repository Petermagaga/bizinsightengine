import pandas as pd
from data_ingestion.models import DataRecord


def get_trends(dataset):

    rows = DataRecord.objects.filter(
        dataset=dataset
    )

    df = pd.DataFrame([
        r.data for r in rows
    ])

    if (
        "production_date"
        not in df.columns
    ):
        return {}

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    trend_data = {}

    for col in numeric_cols[:10]:

        grouped = (
            df.groupby(
                "production_date"
            )[col]
            .sum()
            .to_dict()
        )

        trend_data[col] = grouped

    return trend_data