from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import StudentProfile, TeacherProfile


class DashboardAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        data = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "is_superuser": user.is_superuser,
        }

        if user.role == "teacher":
            profile = TeacherProfile.objects.filter(user=user).first()

            data["teacher"] = {
                "bio": profile.bio if profile else "",
                "expertise": profile.expertise if profile else "",
            }

        elif user.role == "student":
            profile = StudentProfile.objects.filter(user=user).first()

            data["student"] = {
                "roll_number": profile.roll_number if profile else "",
            }

        return Response(data)