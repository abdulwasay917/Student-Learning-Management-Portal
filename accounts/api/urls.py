from django.urls import path
from .views import (
    CreateUserAPI,
    LoginAPI,
    LogoutAPI,
    ForgotPasswordAPI,
    ResetPasswordAPI,
    StudentListAPI
)

urlpatterns = [
    path('create-user/', CreateUserAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('forgot-password/', ForgotPasswordAPI.as_view()),
    path('reset-password/<uidb64>/<token>/', ResetPasswordAPI.as_view()),
    path("students/",StudentListAPI.as_view()),
]