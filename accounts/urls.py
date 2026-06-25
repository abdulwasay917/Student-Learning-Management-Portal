from django.urls import path,include
from .views import (
    login_view,
    create_user_view,
    forgot_password_view,
    reset_password_view,
    student_list_view
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("create-user/", create_user_view, name="create-user"),
    path("forgot-password/", forgot_password_view, name="forgot-password"),
    path("reset-password/<uidb64>/<token>/",reset_password_view,name="reset-password",),
    path("api/", include("accounts.api.urls")),
    path("students/",student_list_view,name="students"),
]