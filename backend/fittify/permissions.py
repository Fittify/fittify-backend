from rest_framework import permissions
from django.contrib.auth.models import User

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user == User.objects.get(pk=view.kwargs['user_id'])