from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .serializers import DashboardSerializer
from .models import Insight
from data_ingestion.models import Dataset
from .dashboard_service import (
    get_dashboard_data
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_insights(request, dataset_id):

    try:
        dataset = Dataset.objects.get(
            id=dataset_id,
            user=request.user
        )

    except Dataset.DoesNotExist:
        return Response(
            {"error": "Dataset not found"},
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
            {"error": "No insights found or access denied "},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        "dataset_id": dataset.id,

        "summary_text":
            insight.summary_text,

        "bi_insights":
            insight.bi_insights,

        "predictions":
            insight.predictions,

        "created_at":
            insight.created_at
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_data(
    request,
    dataset_id
):
    try:
        dataset=Dataset.objects.get(
            id=dataset_id,
            user=request.user
        )
    except Dataset.DoesNotExist:
        return Response(
            {
                "error":"Dataset not found 0r access denied"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    insight =(
        Insight.objects
        .filter(dataset=dataset)
        .order_by("-created_at")
        .first()
    )


    data=DashboardSerializer.build(
        dataset
    )
    return Response(
        data,
        status=status.HTTP_200_OK
    )