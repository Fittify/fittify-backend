from rest_framework import permissions
from django.contrib.auth.models import User

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'user_id' in view.kwargs:
            return request.user == User.objects.get(pk=view.kwargs['user_id'])
        return True