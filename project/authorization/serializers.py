from rest_framework.serializers import Serializer, CharField
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser

class HTTP405MethodNotAllowedSerializer(Serializer):
    """
    Serializer for HTTP 405 Method Not Allowed response.
    """

    detail = CharField()

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "detail",
        )

class UserLoginSerializer(Serializer):
    email = CharField(required=True)
    password = CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError("Пользователь с таким email не найден.")

        if not user.check_password(password):
            raise ValidationError("Неверный пароль.")

        if not user.is_active:
            raise ValidationError("Пользователь не активен.")

        attrs['user'] = user
        return attrs
    
class RefreshTokenSerializer(Serializer):
    refresh = CharField(required=True)

    def validate(self, attrs):
        refresh_token = attrs.get('refresh')

        try:
            refresh = RefreshToken(refresh_token)
            attrs['access_token'] = str(refresh.access_token)
        except Exception as e:
            raise ValidationError(f"Недействительный или просроченный токен обновления: {str(e)}")

        return attrs

    class Meta:
        fields = (
            "refresh",
        )