from rest_framework import permissions
from rest_framework.permissions import BasePermission

from config import settings


class DynamicSerializersMixin:
    serializer_classes_by_action = None

    def get_serializer_class(self):
        if not self.serializer_classes_by_action:
            return self.serializer_class
        return self.serializer_classes_by_action.get(self.action, self.serializer_class)


class APIKeyPermission(BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get('Authorization')
        return api_key == settings.SECRET_API_KEY
