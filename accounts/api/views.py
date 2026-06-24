from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny

from accounts.models import TeacherProfile, StudentProfile

User = get_user_model()


# =========================
# 1. ADMIN ONLY CREATE USER
# =========================
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

        elif role == "student":

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
# =========================
# 2. LOGIN API
# =========================
class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        login(request, user)

        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        })


# =========================
# 3. LOGOUT API
# =========================
class LogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})


# =========================
# 4. FORGOT PASSWORD API
# =========================
class ForgotPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=400)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
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

        return Response({"message": "Reset link sent to email"})


# =========================
# 5. RESET PASSWORD API
# =========================
class ResetPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        password = request.data.get('password')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except:
            return Response({"error": "Invalid link"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        user.set_password(password)
        user.save()

        return Response({"message": "Password reset successful"})