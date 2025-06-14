from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class RegisterView(APIView):
    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: RegisterSerializer,
            400: OpenApiTypes.OBJECT
        },
        description="Register a new user and return JWT tokens.",
        examples=[
            OpenApiExample(
                'Valid Registration Request',
                value={
                    'email': 'user@example.com',
                    'username': 'testuser',
                    'password': 'SecurePass123'
                },
                request_only=True
            ),
            OpenApiExample(
                'Valid Registration Response',
                value={
                    'user': {
                        'email': 'user@example.com',
                        'username': 'testuser'
                    },
                    'tokens': {
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                    }
                },
                response_only=True,
                status_codes=['201']
            ),
            OpenApiExample(
                'Invalid Registration Response',
                value={
                    'email': ['This field is required.'],
                    'password': ['This field may not be blank.']
                },
                response_only=True,
                status_codes=['400']
            )
        ]
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({"user": serializer.data, "tokens": tokens}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT
        },
        description="Authenticate a user and return JWT tokens.",
        examples=[
            OpenApiExample(
                'Valid Login Request',
                value={
                    'email': 'user@example.com',
                    'password': 'SecurePass123'
                },
                request_only=True
            ),
            OpenApiExample(
                'Valid Login Response',
                value={
                    'tokens': {
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                    }
                },
                response_only=True,
                status_codes=['200']
            ),
            OpenApiExample(
                'Invalid Login Response',
                value={
                    'email': ['This field is required.'],
                    'password': ['This field may not be blank.']
                },
                response_only=True,
                status_codes=['400']
            )
        ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = get_tokens_for_user(user)
            return Response({"tokens": tokens}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    responses={
        200: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT
    },
    description="Check if the user is authenticated.",
    auth=['BearerAuth'],
    examples=[
        OpenApiExample(
            'Authenticated Response',
            value={
                'authenticated': True,
                'email': 'user@example.com',
                'username': 'testuser'
            },
            response_only=True,
            status_codes=['200']
        ),
        OpenApiExample(
            'Unauthenticated Response',
            value={
                'authenticated': False
            },
            response_only=True,
            status_codes=['401']
        )
    ]
)
@api_view(['GET'])
def auth_status(request):
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'email': request.user.email,
            'username': request.user.username,
        })
    return Response({'authenticated': False}, status=status.HTTP_401_UNAUTHORIZED)