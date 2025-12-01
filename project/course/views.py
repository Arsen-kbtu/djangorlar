from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from .serializers import (
    CourseListSerializer,
    CourseCreateSerializer,
    CourseUpdateSerializer,
    CourseDeleteSerializer,
    LessonBaseSerializer,
)

from .permissions import IsOwnerOrReadOnly

from .models import Course, Lesson

from decimal import Decimal


# Create your views here.
class CourseViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def list_courses(self, request: Request) -> Response:
        courses = Course.objects.filter(deleted_at__isnull=True)
        serializer = CourseListSerializer(courses, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def retrieve_course(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        serializer = CourseListSerializer(course)
        return Response(data=serializer.data, status=HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def create_course(self, request: Request) -> Response:
        serializer = CourseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = serializer.save(owner=request.user)
        return Response(data=CourseListSerializer(course).data, status=HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["put", "patch"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def update_course(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        self.check_object_permissions(request, course)
        if course.owner != request.user:
            return Response(status=HTTP_403_FORBIDDEN)
        serializer = CourseUpdateSerializer(
            course, data=request.data, partial=(request.method == "PATCH")
        )
        serializer.is_valid(raise_exception=True)
        course = serializer.save()
        return Response(data=CourseListSerializer(course).data, status=HTTP_200_OK)

    @action(
        detail=True,
        methods=["delete"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def delete_course(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        serializer = CourseDeleteSerializer(course)
        course.deleted_at = datetime.now()
        course.save()
        return Response(data=serializer.data, status=HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def activate_course(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        course.is_active = True
        course.save()
        return Response(data=CourseListSerializer(course).data, status=HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def deactivate_course(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        course.is_active = False
        course.save()
        return Response(data=CourseListSerializer(course).data, status=HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def list_lessons(self, request: Request, pk: int) -> Response:
        course = Course.objects.get(pk=pk, deleted_at__isnull=True)
        lessons = course.lessons.filter(deleted_at__isnull=True)
        serializer = LessonBaseSerializer(lessons, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)


class LessonViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    # Lesson viewset methods would go here

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def create_lesson(self, request: Request) -> Response:
        serializer = LessonBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lesson = serializer.save()
        return Response(data=LessonBaseSerializer(lesson).data, status=HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["put"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def move_lesson(self, request: Request, pk: int) -> Response:
        """
        Move lesson to new position.
        """
        lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
        before_lesson_id = request.data.get("before_lesson_id")

        # Получаем все уроки курса, отсортированные по order
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
            lesson.indentation = 0  # Сброс indentation
        else:
            # Вставить перед before_lesson
            before_lesson = Lesson.objects.get(
                pk=before_lesson_id, deleted_at__isnull=True
            )

            # Найти урок перед before_lesson
            previous_lessons = lessons.filter(order__lt=before_lesson.order)

            if previous_lessons.exists():
                previous_lesson = previous_lessons.last()
                # Вставить между previous и before
                lesson.order = (previous_lesson.order + before_lesson.order) / 2
                # Установить indentation как у before_lesson
                lesson.indentation = before_lesson.indentation
            else:
                # before_lesson первый, вставить перед ним
                lesson.order = before_lesson.order / 2
                lesson.indentation = 0

        lesson.save()

        return Response(
            data={"order": str(lesson.order), "indentation": lesson.indentation},
            status=HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["delete"],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def delete_lesson(self, request: Request, pk: int) -> Response:
        lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
        lesson.deleted_at = datetime.now()
        lesson.save()
        return Response(data=LessonBaseSerializer(lesson).data, status=HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],  # ← Должно быть POST
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def publish_lesson(self, request: Request, pk: int) -> Response:
        lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
        lesson.is_published = True
        lesson.save()
        return Response(data=LessonBaseSerializer(lesson).data, status=HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],  # ← Должно быть POST
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
    )
    def unpublish_lesson(self, request: Request, pk: int) -> Response:
        lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
        lesson.is_published = False
        lesson.save()
        return Response(data=LessonBaseSerializer(lesson).data, status=HTTP_200_OK)
