from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer
from core.utils.response import success_response,error_response


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer=RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return success_response(message="User registered successfully",data=serializer.data,status_code=201)
    return error_response(message="Registration failed",data=serializer.errors)


