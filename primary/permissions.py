from rest_framework.permissions import BasePermission
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .models import *

class IsUserOrAdminForDelete(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
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
    

    