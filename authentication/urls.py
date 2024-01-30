from .views import ( 
    UserRegistrationView,
    UserLoginView,
    UserChangePasswordView

)
from rest_framework_simplejwt.views import  TokenRefreshView
from django.urls import path


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegistrationView.as_view(),name='user-register'),
    path('login/',UserLoginView.as_view(),name='use-login'),
    path('change-password/',UserChangePasswordView.as_view(),name="user-change-password"),



]