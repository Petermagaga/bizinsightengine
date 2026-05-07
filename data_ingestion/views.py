from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .serializers import DatasetSerializer
from analytics.tasks import process_dataset_task


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_dataset(request):

    print(request.data)
    print(request.FILES)

    serializer = DatasetSerializer(data=request.data)

    if not serializer.is_valid():
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    dataset = serializer.save(user=request.user)

    process_dataset_task.delay(dataset.id)

    return Response(
        {
            "message": "Dataset uploaded successfully. Processing started.",
            "dataset_id": dataset.id
        },
        status=status.HTTP_201_CREATED
    )


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