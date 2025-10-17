from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow access to users whose role is 'student'.
    This assumes your custom User model has a 'role' field.
    """
    message = 'Access denied. Only users with the role of "student" can perform this action.'

    def has_permission(self, request, view):
        # Check if user is authenticated and is a student
        if request.user.is_authenticated and hasattr(request.user, 'role'):
            return request.user.role == 'student'
        return False