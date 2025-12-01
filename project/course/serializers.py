from rest_framework.serializers import Serializer, CharField, ModelSerializer, SerializerMethodField
from rest_framework.exceptions import ValidationError

from authorization.models import CustomUser
from .models import Course, Lesson

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

class OwnerSerializer(ModelSerializer):
    """
    Serializer for representing the owner (User).
    Similar to CustomUserForeignSerializer.
    """
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "first_name",
        )

class CourseBaseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        

class CourseListSerializer(CourseBaseSerializer):
    """
    Serializer for listing Course instances.
    """

    owner = OwnerSerializer()
    lesson_count = SerializerMethodField(method_name='get_lesson_count')

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
            "owner",
            "lesson_count",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def get_lesson_count(self, obj: Course) -> int:
        return obj.lessons.filter(deleted_at__isnull=True).count()

class CourseCreateSerializer(CourseBaseSerializer):
    pass

class CourseUpdateSerializer(CourseBaseSerializer):
    '''
    Serializer for updating Course instances.
    
    Allows partial updates.
    '''
    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "is_active",
        )

class CourseDeleteSerializer(Serializer):
    """
    Serializer for deleting Course instances.
    """

    class Meta:
        """Customization of the Serializer metadata."""

        fields = ()

class LessonBaseSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class LessonListSerializer(LessonBaseSerializer):
    """
    Serializer for listing Lesson instances.
    """

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Lesson
        fields = (
            "id",
            "title",
            "content",
            "is_published",
            "created_at",
            "updated_at",
            "deleted_at",
            "course",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

class LessonCreateSerializer(LessonBaseSerializer):
    pass
