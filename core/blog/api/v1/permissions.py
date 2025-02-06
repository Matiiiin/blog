from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsVerifiedUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_verified is False:
            raise PermissionDenied('Please verify your email address first.')
        return True

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.author != request.user.profile:
            raise PermissionDenied('You are not the owner of this object.')
        return True