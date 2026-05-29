import logging
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import (
    Response
)
from rest_framework import status

from .models import Insight
from data_ingestion.models import Dataset
from .dashboard_service import (
    get_dashboard_data
)
from .serializers import InsightSerializer


logger = logging.getLogger(__name__)
# -----------------------------------
# Get Raw Insight Data
# -----------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_insights(
    request,
    dataset_id
):
    try:
        dataset = Dataset.objects.get(
            id=dataset_id,
            user=request.user
        )

    except Dataset.DoesNotExist:
        return Response(
            {
                "error":
                "Dataset not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    insight = (
        Insight.objects
        .filter(dataset=dataset)
        .order_by("-created_at")
        .first()
    )

    if not insight:
        return Response(
            {
                "error":
                "No insights found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(
        {
            "dataset_id":
                dataset.id,

            "summary_text":
                insight.summary_text,

            "bi_insights":
                insight.bi_insights,

            "predictions":
                insight.predictions,

            "created_at":
                insight.created_at
        },
        status=status.HTTP_200_OK
    )


# -----------------------------------
# Dashboard Endpoint
# -----------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_data(
    request,
    dataset_id
):
    
    try:
        dataset = Dataset.objects.get(
            id=dataset_id,
            user=request.user
        )

    except Dataset.DoesNotExist:
        return Response(
            {
                "error":
                "Dataset not found or access denied"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        dashboard = get_dashboard_data(
            dataset
        )

        return Response(
            dashboard,
            status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.exception(
            "Dashboard error"
        )

        return Response(
            {
                "error":
                "Dashboard"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def health_check(request):

    return Response(
        {
            "status":
                "healthy",

            "service":
                "insights-api"
        }
    )