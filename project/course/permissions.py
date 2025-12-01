from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Works with Course (has owner) and Lesson (has course.owner).
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # Write permissions are only allowed to the owner
        # Для Course проверяем obj.owner
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        # Для Lesson проверяем obj.course.owner
        if hasattr(obj, 'course'):
            return obj.course.owner == request.user
        
        return False