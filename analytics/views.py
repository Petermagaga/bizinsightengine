from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Dataset


@api_view(['GET'])
def dataset_status(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id)
    except Dataset.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    return Response({
        "id": dataset.id,
        "status": dataset.status,
        "progress": dataset.progress
    })

