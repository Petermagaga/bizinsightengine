from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import DatasetSerializer
from analytics.tasks import process_dataset_task


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_dataset(request):
    serializer = DatasetSerializer(data=request.data)

    if not serializer.is_valid():
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