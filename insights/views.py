from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .models import Insight
from .serializers import InsightSerializer
from data_ingestion.models import Dataset



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_insights(request,dataset_id):
    try:
        dataset=Dataset.objects.get(id=dataset_id)
    except Dataset.DoesNotExist:
        return Response({"error":"Dataset not found"}, status=status.HTTP_404_NOT_FOUND)
    insights =Insight.objects.filter(dataset=dataset).order_by('-created_at')
    serializer =InsightSerializer(insights,many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)

