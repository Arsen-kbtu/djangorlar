# Django modules
from django.urls import include, path

# Django Rest Framework modules
from rest_framework.routers import DefaultRouter

# Project modules
from .views import CourseViewSet, LessonViewSet


router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(
    prefix="courses",
    viewset=CourseViewSet,
    basename="course"
)

router.register(
    prefix="lessons",
    viewset=LessonViewSet,
    basename="lesson"
)

urlpatterns = [
    path("v1/", include(router.urls)),
]