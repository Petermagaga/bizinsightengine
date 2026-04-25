from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Dataset,DataRecord
from .serializers import DatasetSerializer
from .utils import parse_excel
from analytics.tasks import process_dataset_task


@api_view(['GET','POST'])
def upload_dataset(request):
    serializer=DatasetSerializer(data=request.data)


    if serializer.is_valid():
        dataset = serializer.save(user=request.user if request.user.is_authenticated else None)
        process_dataset_task.delay(dataset.id)
        
        try:
            parsed_data =parse_excel(dataset.file)

            for row in parsed_data:
                DataRecord.objects.create(dataset=dataset,data=row)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
