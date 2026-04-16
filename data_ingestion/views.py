from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Dataset
from .serializers import DatasetSerializer

@api_view(['POST'])
def upload_dataset(request):
    serializer=DatasetSerializer(data=request.data)


    if serializer.is_valid():
        serializer.save(user=request.user if request.user.is_authenticated else None)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
