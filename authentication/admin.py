from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
        list_display=['id','fullname','email','username','is_active','is_staff','is_superuser']
        list_per_page=10
        search_fields=['first_name__icontains']
        add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name","last_name","email","username", "password1", "password2"),
            },
        ),
    )
        
        def fullname(self,user):
                return f"{user.first_name} {user.last_name}"
        



