from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    IsAuthenticated
)

from accounts.models import TeacherProfile, StudentProfile

User = get_user_model()


class CreateUserAPI(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):

        data = request.data

        role = data.get("role")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        phone = data.get("phone")

        if not role:
            return Response(
                {"error": "Role is required"},
                status=400
            )

        if role not in ["teacher", "student"]:
            return Response(
                {"error": "Invalid role"},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=400
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=400
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            name=name,
            phone=phone,
            role=role
        )

        if role == "teacher":

            TeacherProfile.objects.create(
                user=user,
                bio=data.get("bio", ""),
                expertise=data.get("expertise", "")
            )

        else:

            StudentProfile.objects.create(
                user=user,
                roll_number=data.get("roll_number")
            )

        return Response(
            {
                "message": f"{role.title()} created successfully",
                "user_id": user.id
            },
            status=201
        )


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=400
            )

        login(request, user)

        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        })


class LogoutAPI(APIView):

    def post(self, request):

        logout(request)

        return Response({
            "message": "Logged out successfully"
        })


class ForgotPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=400
            )

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(user)

        link = request.build_absolute_uri(
            f"/accounts/reset-password/{uid}/{token}/"
        )

        send_mail(
            "Reset Password",
            f"Click here to reset password: {link}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        return Response({
            "message": "Reset link sent to email"
        })


class ResetPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):

        password = request.data.get("password")

        try:
            uid = urlsafe_base64_decode(
                uidb64
            ).decode()

            user = User.objects.get(pk=uid)

        except Exception:
            return Response(
                {"error": "Invalid link"},
                status=400
            )

        if not default_token_generator.check_token(
            user,
            token
        ):
            return Response(
                {"error": "Invalid or expired token"},
                status=400
            )

        user.set_password(password)
        user.save()

        return Response({
            "message": "Password reset successful"
        })


class StudentListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role == "student":
            return Response(
                {"error": "Forbidden"},
                status=403
            )

        students = StudentProfile.objects.select_related(
            "user"
        ).filter(
            user__is_superuser=False
        )

        data = [
            {
                "id": s.id,
                "user_id": s.user.id,
                "name": s.user.name,
                "username": s.user.username,
                "email": s.user.email,
                "phone": s.user.phone,
                "roll_number": s.roll_number,
            }
            for s in students
        ]

        return Response({
            "is_superuser": request.user.is_superuser,
            "students": data
        })


class TeacherListAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):

        teachers = TeacherProfile.objects.select_related(
            "user"
        ).filter(
            user__is_superuser=False
        )

        data = [
            {
                "id": t.id,
                "user_id": t.user.id,
                "name": t.user.name,
                "username": t.user.username,
                "email": t.user.email,
                "phone": t.user.phone,
                "bio": t.bio,
                "expertise": t.expertise,
            }
            for t in teachers
        ]

        return Response(data)


class DeleteUserAPI(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, user_id):

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=404
            )

        if user.is_superuser:
            return Response(
                {"error": "Superuser cannot be deleted"},
                status=403
            )

        user.delete()

        return Response({
            "message": "User deleted successfully"
        })