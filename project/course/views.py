from datetime import datetime
from decimal import Decimal
from typing import Any

# Django REST Framework
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST
)
from rest_framework import serializers

# DRF Spectacular
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    inline_serializer
)

# Project modules
from .serializers import (
    CourseListSerializer,
    CourseCreateSerializer,
    CourseUpdateSerializer,
    CourseDeleteSerializer,
    LessonBaseSerializer,
)
from .permissions import IsOwnerOrReadOnly
from .models import Course, Lesson


class CourseViewSet(ViewSet):
    """
    ViewSet для управления курсами.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Список курсов",
        description="Получить список всех не удаленных курсов. Можно фильтровать по статусу активности.",
        parameters=[
            OpenApiParameter(
                name="is_active",
                description="Фильтр по активности (true/false)",
                required=False,
                type=bool
            )
        ],
        responses={200: CourseListSerializer(many=True)},
        tags=["Courses"]
    )
    @action(detail=False, methods=["get"])
    def list_courses(self, request: Request) -> Response:
        courses = Course.objects.filter(deleted_at__isnull=True)
        
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            courses = courses.filter(is_active=is_active_bool)

        serializer = CourseListSerializer(courses, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)

    @extend_schema(
        summary="Получить курс",
        description="Получить детальную информацию о курсе по ID.",
        responses={200: CourseListSerializer},
        tags=["Courses"]
    )
    @action(detail=True, methods=["get"])
    def retrieve_course(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        serializer = CourseListSerializer(course)
        return Response(data=serializer.data, status=HTTP_200_OK)

    @extend_schema(
        summary="Создать курс",
        description="Создать новый курс. Владелец устанавливается автоматически.",
        request=CourseCreateSerializer,
        responses={201: CourseListSerializer},
        tags=["Courses"]
    )
    @action(detail=False, methods=["post"])
    def create_course(self, request: Request) -> Response:
        serializer = CourseCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        course = serializer.save(owner=request.user)
        return Response(data=CourseListSerializer(course).data, status=HTTP_201_CREATED)

    @extend_schema(
        summary="Обновить курс",
        description="Полное или частичное обновление курса. Доступно только владельцу.",
        request=CourseUpdateSerializer,
        responses={200: CourseListSerializer},
        tags=["Courses"]
    )
    @action(
        detail=True,
        methods=["put", "patch"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def update_course(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        self.check_object_permissions(request, course)
        
        serializer = CourseUpdateSerializer(
            course, data=request.data, partial=(request.method == "PATCH")
        )
        serializer.is_valid(raise_exception=True)
        course = serializer.save()
        return Response(data=CourseListSerializer(course).data, status=HTTP_200_OK)

    @extend_schema(
        summary="Удалить курс",
        description="Мягкое удаление курса. Доступно только владельцу.",
        responses={204: None},
        tags=["Courses"]
    )
    @action(
        detail=True,
        methods=["delete"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def delete_course(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        self.check_object_permissions(request, course)
        
        course.deleted_at = datetime.now()
        course.save()
        return Response(status=HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Активировать курс",
        description="Сделать курс активным. Доступно только владельцу.",
        responses={
            200: CourseListSerializer,
            400: OpenApiResponse(description="Course is already active")
        },
        tags=["Courses"]
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def activate_course(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        self.check_object_permissions(request, course)
        
        if course.is_active:
            return Response({"detail": "Course is already active"}, status=HTTP_400_BAD_REQUEST)

        course.is_active = True
        course.save()
        return Response(data=CourseListSerializer(course).data, status=HTTP_200_OK)

    @extend_schema(
        summary="Деактивировать курс",
        description="Сделать курс неактивным. Доступно только владельцу.",
        responses={
            200: CourseListSerializer,
            400: OpenApiResponse(description="Course is already inactive")
        },
        tags=["Courses"]
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def deactivate_course(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        self.check_object_permissions(request, course)

        if not course.is_active:
            return Response({"detail": "Course is already inactive"}, status=HTTP_400_BAD_REQUEST)

        course.is_active = False
        course.save()
        return Response(data=CourseListSerializer(course).data, status=HTTP_200_OK)

    @extend_schema(
        summary="Список уроков курса",
        description="Получить список всех уроков конкретного курса.",
        responses={200: LessonBaseSerializer(many=True)},
        tags=["Courses"]
    )
    @action(detail=True, methods=["get"])
    def list_lessons(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        lessons = course.lessons.filter(deleted_at__isnull=True).order_by('order')
        serializer = LessonBaseSerializer(lessons, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)


class LessonViewSet(ViewSet):
    """
    ViewSet для управления уроками.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Создать урок",
        description="Создать новый урок в курсе. Порядок определяется автоматически.",
        request=LessonBaseSerializer,
        responses={201: LessonBaseSerializer},
        tags=["Lessons"]
    )
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def create_lesson(self, request: Request) -> Response:
        # Валидация данных
        serializer = LessonBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Получаем курс для проверки прав и расчета порядка
        course = serializer.validated_data['course']
        
        # Проверяем права на курс (так как у урока еще нет ID)
        if course.owner != request.user:
             return Response({"detail": "You do not have permission to add lessons to this course."}, status=HTTP_403_FORBIDDEN)

        # Расчет порядка (вставка в начало)
        first_lesson = Lesson.objects.filter(
            course=course, 
            deleted_at__isnull=True
        ).order_by('order').first()
        
        if first_lesson:
            new_order = first_lesson.order / 2
        else:
            new_order = Decimal('1.00')

        lesson = serializer.save(order=new_order)
        return Response(data=LessonBaseSerializer(lesson).data, status=HTTP_201_CREATED)

    @extend_schema(
        summary="Переместить урок",
        description="Изменить порядок урока. Пересчитывает отступы (indentation).",
        request=inline_serializer(
            name='MoveLessonRequest',
            fields={
                'before_lesson_id': serializers.IntegerField(allow_null=True, required=False, help_text="ID урока, перед которым нужно вставить. Null - в конец.")
            }
        ),
        responses={
            200: inline_serializer(
                name='MoveLessonResponse',
                fields={
                    'order': serializers.CharField(),
                    'indentation': serializers.IntegerField()
                }
            )
        },
        tags=["Lessons"]
    )
    @action(
        detail=True,
        methods=["put"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def move_lesson(self, request: Request, pk: int) -> Response:
        lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
        self.check_object_permissions(request, lesson)
        
        before_lesson_id = request.data.get("before_lesson_id")

        lessons = (
            Lesson.objects.filter(course=lesson.course, deleted_at__isnull=True)
            .exclude(id=lesson.id)
            .order_by("order")
        )

        if before_lesson_id is None:
            # Стать последним
            last_lesson = lessons.last()
            if last_lesson:
                lesson.order = last_lesson.order + Decimal("1.00")
            else:
                lesson.order = Decimal("1.00")
            lesson.indentation = 0
        else:
            # Вставить перед before_lesson
            before_lesson = Lesson.objects.get(
                pk=before_lesson_id, deleted_at__isnull=True
            )

            previous_lessons = lessons.filter(order__lt=before_lesson.order)

            if previous_lessons.exists():
                previous_lesson = previous_lessons.last()
                lesson.order = (previous_lesson.order + before_lesson.order) / 2
                lesson.indentation = before_lesson.indentation
            else:
                lesson.order = before_lesson.order / 2
                lesson.indentation = 0

        lesson.save()

        return Response(
            data={"order": str(lesson.order), "indentation": lesson.indentation},
            status=HTTP_200_OK,
        )

    @extend_schema(
        summary="Удалить урок",
        description="Мягкое удаление урока.",
        responses={204: None},
        tags=["Lessons"]
    )
    @action(
        detail=True,
        methods=["delete"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def delete_lesson(self, request: Request, pk: int) -> Response:
        lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
        self.check_object_permissions(request, lesson)
        
        lesson.deleted_at = datetime.now()
        lesson.save()
        return Response(status=HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Опубликовать урок",
        description="Установить статус is_published = True.",
        responses={200: LessonBaseSerializer},
        tags=["Lessons"]
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def publish_lesson(self, request: Request, pk: int) -> Response:
        lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
        self.check_object_permissions(request, lesson)
        
        lesson.is_published = True
        lesson.save()
        return Response(data=LessonBaseSerializer(lesson).data, status=HTTP_200_OK)

    @extend_schema(
        summary="Снять урок с публикации",
        description="Установить статус is_published = False.",
        responses={200: LessonBaseSerializer},
        tags=["Lessons"]
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def unpublish_lesson(self, request: Request, pk: int) -> Response:
        lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
        self.check_object_permissions(request, lesson)
        
        lesson.is_published = False
        lesson.save()
        return Response(data=LessonBaseSerializer(lesson).data, status=HTTP_200_OK)
