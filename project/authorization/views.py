from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.status import HTTP_200_OK

from .serializers import RefreshTokenSerializer, UserLoginSerializer

# Create your views here.
class CustomUserViewSet(ViewSet):
    @action(detail=False, methods=['post'], url_path='login', url_name='login', permission_classes=[AllowAny])
    def login(self, request: Request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response(
            data={
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        },
        status=HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'], url_path='refresh', url_name='refresh', permission_classes=[AllowAny])
    def refresh(self, request: Request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            data={
                'access_token': str(serializer.validated_data['access_token']),
                
            },
            status=HTTP_200_OK
        )