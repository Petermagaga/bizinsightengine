from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Dataset


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dataset_status(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
    except Dataset.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    return Response({
        "id": dataset.id,
        "name": dataset.name,
        "status": dataset.status,
        "progress": getattr(dataset, "progress", 0),
        "uploaded_at": dataset.uploaded_at,
    })