import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Course, Lesson

User = get_user_model()


@pytest.fixture
def api_client():
    """Fixture для API клиента."""
    return APIClient()


@pytest.fixture
def user(db):
    """Fixture для создания пользователя."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        first_name="Test User"
    )


@pytest.fixture
def another_user(db):
    """Fixture для создания второго пользователя."""
    return User.objects.create_user(
        username="anotheruser",
        email="another@example.com",
        password="testpass123",
        first_name="Another User"
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Fixture для аутентифицированного клиента."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def course(user):
    """Fixture для создания курса."""
    return Course.objects.create(
        title="Test Course",
        description="Test Description",
        owner=user,
        is_active=True
    )


@pytest.fixture
def lesson(course):
    """Fixture для создания урока."""
    return Lesson.objects.create(
        title="Test Lesson",
        content="Test Content",
        course=course,
        order=Decimal("1.00"),
        indentation=0
    )


# ==================== AUTHENTICATION TESTS ====================

@pytest.mark.django_db
class TestAuthentication:
    """Тесты для эндпоинтов аутентификации."""

    def test_login_success(self, api_client, user):
        """Тест успешного логина с валидными данными."""
        url = "/auth/v1/users/login"
        data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        response = api_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["email"] == "test@example.com"

    def test_login_invalid_credentials(self, api_client, user):
        """Тест логина с невалидными данными."""
        url = "/auth/v1/users/login"
        data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        response = api_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_refresh_token_success(self, api_client, user):
        """Тест успешного обновления токена."""
        # Сначала получаем токены
        login_url = "/auth/v1/users/login"
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        login_response = api_client.post(login_url, login_data, format="json")
        refresh_token = login_response.data["refresh"]
        
        # Обновляем access token
        refresh_url = "/auth/v1/users/refresh"
        refresh_data = {"refresh": refresh_token}
        
        response = api_client.post(refresh_url, refresh_data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data

    def test_refresh_token_invalid(self, api_client):
        """Тест обновления токена с невалидным refresh token."""
        url = "/auth/v1/users/refresh"
        data = {"refresh": "invalid_token"}
        
        response = api_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ==================== COURSE TESTS ====================

@pytest.mark.django_db
class TestCourseEndpoints:
    """Тесты для эндпоинтов курсов."""

    def test_list_courses_success(self, authenticated_client, course):
        """Тест получения списка курсов."""
        url = "/course/v1/courses/list_courses"
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == "Test Course"

    def test_list_courses_filter_active(self, authenticated_client, user):
        """Тест фильтрации курсов по is_active."""
        # Создаем активный и неактивный курсы
        Course.objects.create(title="Active", owner=user, is_active=True)
        Course.objects.create(title="Inactive", owner=user, is_active=False)
        
        url = "/course/v1/courses/list_courses?is_active=true"
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["is_active"] is True

    def test_create_course_success(self, authenticated_client):
        """Тест успешного создания курса."""
        url = "/course/v1/courses/create_course"
        data = {
            "title": "New Course",
            "description": "New Description",
            "is_active": True,
            "owner": authenticated_client.handler._force_user.id
        }
        
        response = authenticated_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Course"
        assert Course.objects.count() == 1

    def test_create_course_missing_title(self, authenticated_client):
        """Тест создания курса без обязательного поля title."""
        url = "/course/v1/courses/create_course"
        data = {
            "description": "No Title"
        }
        
        response = authenticated_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_course_success(self, authenticated_client, course):
        """Тест получения одного курса."""
        url = f"/course/v1/courses/{course.id}/retrieve_course"
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Test Course"

    def test_update_course_success(self, authenticated_client, course):
        """Тест обновления курса владельцем."""
        url = f"/course/v1/courses/{course.id}/update_course"
        data = {"title": "Updated Title"}
        
        response = authenticated_client.put(url, data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated Title"

    def test_update_course_not_owner(self, api_client, another_user, course):
        """Тест обновления курса не владельцем."""
        api_client.force_authenticate(user=another_user)
        url = f"/course/v1/courses/{course.id}/update_course"
        data = {"title": "Hacked"}
        
        response = api_client.put(url, data, format="json")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_course_success(self, authenticated_client, course):
        """Тест мягкого удаления курса."""
        url = f"/course/v1/courses/{course.id}/delete_course"
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        course.refresh_from_db()
        assert course.deleted_at is not None

    def test_activate_course_success(self, authenticated_client, course):
        """Тест активации неактивного курса."""
        course.is_active = False
        course.save()
        
        url = f"/course/v1/courses/{course.id}/activate_course"
        
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        course.refresh_from_db()
        assert course.is_active is True

    def test_activate_already_active_course(self, authenticated_client, course):
        """Тест активации уже активного курса."""
        url = f"/course/v1/courses/{course.id}/activate_course"
        
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK


# ==================== LESSON TESTS ====================

@pytest.mark.django_db
class TestLessonEndpoints:
    """Тесты для эндпоинтов уроков."""

    def test_create_lesson_success(self, authenticated_client, course):
        """Тест успешного создания урока."""
        url = "/course/v1/lessons/create_lesson"
        data = {
            "title": "New Lesson",
            "content": "Lesson Content",
            "course": course.id
        }
        
        response = authenticated_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Lesson"
        assert Lesson.objects.count() == 1

    def test_create_lesson_missing_title(self, authenticated_client, course):
        """Тест создания урока без title."""
        url = "/course/v1/lessons/create_lesson"
        data = {
            "content": "No Title",
            "course": course.id
        }
        
        response = authenticated_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_lesson_success(self, authenticated_client, lesson):
        """Тест мягкого удаления урока."""
        url = f"/course/v1/lessons/{lesson.id}/delete_lesson"
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        lesson.refresh_from_db()
        assert lesson.deleted_at is not None

    def test_publish_lesson_success(self, authenticated_client, lesson):
        """Тест публикации урока."""
        url = f"/course/v1/lessons/{lesson.id}/publish_lesson"
        
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        lesson.refresh_from_db()
        assert lesson.is_published is True

    def test_move_lesson_to_end(self, authenticated_client, lesson, course):
        """Тест перемещения урока в конец."""
        # Создаем еще один урок
        Lesson.objects.create(
            title="Second",
            content="Content",
            course=course,
            order=Decimal("2.00")
        )
        
        url = f"/course/v1/lessons/{lesson.id}/move_lesson"
        data = {"before_lesson_id": None}
        
        response = authenticated_client.put(url, data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        lesson.refresh_from_db()
        assert lesson.order > Decimal("2.00")
