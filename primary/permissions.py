from rest_framework.permissions import BasePermission
from rest_framework import permissions
from .models import *

class IsUserOrAdminForDelete(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
    
class ReviewAndReplyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['POST','DELETE']:
            return request.user.is_authenticated
        return request.user.is_staff
        

class IsUserOrAdminOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user or request.user.is_staff:
            return True 
        return False
    

class IsNormalUserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser
    
    def has_permission(self, request, view):
        if request.user.is_staff and (not request.user.is_superuser):
            return False
        return request.user or request.user.is_superuser


    

    