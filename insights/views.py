from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .models import Insight
from data_ingestion.models import Dataset


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
            {"error": "No insights found"},
            status=404
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