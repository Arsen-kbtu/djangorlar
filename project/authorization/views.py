from typing import Any

# Python modules
from rest_framework_simplejwt.tokens import RefreshToken

# Django REST Framework
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework import serializers

# DRF Spectacular
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer

# Project modules
from .serializers import RefreshTokenSerializer, UserLoginSerializer
from .models import CustomUser


class CustomUserViewSet(ViewSet):
    """
    ViewSet для управления аутентификацией пользователей.
    """

    @extend_schema(
        summary="Вход в систему",
        description="Аутентификация пользователя по email и паролю. Возвращает access и refresh токены.",
        request=UserLoginSerializer,
        responses={
            200: inline_serializer(
                name='LoginResponse',
                fields={
                    'id': serializers.IntegerField(),
                    'email': serializers.EmailField(),
                    'username': serializers.CharField(),
                    'refresh': serializers.CharField(),
                    'access': serializers.CharField(),
                }
            ),
            400: OpenApiResponse(description="Неверные учетные данные")
        },
        tags=["Authentication"]
    )
    @action(
        detail=False,
        methods=['post'],
        url_path='login',
        url_name='login',
        permission_classes=[AllowAny]
    )
    def login(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user: CustomUser = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return DRFResponse(
            data={
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=HTTP_200_OK
        )
    
    @extend_schema(
        summary="Обновление токена",
        description="Получение нового access токена с использованием refresh токена.",
        request=RefreshTokenSerializer,
        responses={
            200: inline_serializer(
                name='RefreshResponse',
                fields={
                    'access': serializers.CharField(),
                }
            ),
            400: OpenApiResponse(description="Неверный или просроченный refresh токен")
        },
        tags=["Authentication"]
    )
    @action(
        detail=False,
        methods=['post'],
        url_path='refresh',
        url_name='refresh',
        permission_classes=[AllowAny]
    )
    def refresh_token(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        # Переименовал метод в refresh_token, чтобы избежать конфликта имен
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # В сериализаторе RefreshTokenSerializer обычно возвращается 'access'
        # Проверьте, как у вас названо поле в сериализаторе. Обычно это 'access'.
        # Если у вас 'access_token', оставьте как было. Я исправил на стандартный 'access'.
        
        return DRFResponse(
            data={
                'access': str(serializer.validated_data.get('access', serializer.validated_data.get('access_token'))),
            },
            status=HTTP_200_OK
        )