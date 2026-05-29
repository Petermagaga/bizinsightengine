from .models import Insight
from .groq_service import (
    generate_dashboard_ai
)

from data_ingestion.models import (
    DataRecord
)


def generate_insights_for_dataset(
    dataset
):

    records = list(
        DataRecord.objects.filter(
            dataset=dataset
        ).values_list(
            "data",
            flat=True
        )
    )

    if not records:

        return {
            "error":
            "No records found"
        }

    dashboard_data = (
        generate_dashboard_ai(
            records
        )
    )

    Insight.objects.filter(
        dataset=dataset
    ).delete()

    insight = Insight.objects.create(
        dataset=dataset,
        summary_text=(
            dashboard_data
            .get("summary", {})
            .get(
                "headline",
                ""
            )
        ),
        dashboard_data=dashboard_data
    )

    return insight.id