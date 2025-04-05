from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def auth_status(request):
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'email': request.user.email,
            'username': request.user.username,
        })
    return Response({'authenticated': False}, status=status.HTTP_401_UNAUTHORIZED)