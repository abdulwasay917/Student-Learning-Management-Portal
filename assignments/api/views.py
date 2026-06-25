from rest_framework.views import APIView
from rest_framework.response import Response

from assignments.models import (
    Assignment,
    Submission
)

from assignments.api.serializers import (
    AssignmentSerializer,
    SubmissionSerializer
)

from accounts.models import (
    StudentProfile
)


# =========================
# LIST ASSIGNMENTS
# =========================

class AssignmentListAPI(APIView):

    def get(self, request):

        assignments = Assignment.objects.all().order_by(
            "-created_at"
        )

        serializer = AssignmentSerializer(
            assignments,
            many=True
        )

        return Response(serializer.data)


# =========================
# CREATE ASSIGNMENT
# =========================

class CreateAssignmentAPI(APIView):

    def post(self, request):

        if not (
            request.user.role == "teacher"
            or request.user.is_superuser
        ):
            return Response(
                {"error": "Permission denied"},
                status=403
            )

        serializer = AssignmentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                created_by=request.user
            )

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )

# =========================
# DELETE ASSIGNMENT
# =========================

class DeleteAssignmentAPI(APIView):

    def delete(self, request, pk):

        try:
            assignment = Assignment.objects.get(
                pk=pk
            )

        except Assignment.DoesNotExist:
            return Response(
                {"error": "Assignment not found"},
                status=404
            )

        if not (
            request.user.is_superuser
            or assignment.created_by == request.user
        ):
            return Response(
                {"error": "Not allowed"},
                status=403
            )

        assignment.delete()

        return Response(
            {"message": "Assignment deleted"},
            status=200
        )


# =========================
# SUBMIT ASSIGNMENT
# =========================

class SubmitAssignmentAPI(APIView):

    def post(self, request, pk):

        if request.user.role != "student":
            return Response(
                {"error": "Only students can submit"},
                status=403
            )

        try:
            assignment = Assignment.objects.get(
                pk=pk
            )

        except Assignment.DoesNotExist:
            return Response(
                {"error": "Assignment not found"},
                status=404
            )

        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "File is required"},
                status=400
            )

        submission, created = (
            Submission.objects.update_or_create(
                assignment=assignment,
                student=request.user,
                defaults={
                    "file": file
                }
            )
        )

        serializer = SubmissionSerializer(
            submission
        )

        return Response(
            serializer.data,
            status=201
        )


# =========================
# SUBMITTED STUDENTS
# =========================

class SubmittedStudentsAPI(APIView):

    def get(self, request, pk):

        try:
            assignment = Assignment.objects.get(
                pk=pk
            )

        except Assignment.DoesNotExist:
            return Response(
                {"error": "Assignment not found"},
                status=404
            )

        submissions = Submission.objects.filter(
            assignment=assignment
        ).select_related(
            "student"
        )

        data = []

        for submission in submissions:

            profile = StudentProfile.objects.filter(
                user=submission.student
            ).first()

            data.append({
                "submission_id": submission.id,
                "student_name": submission.student.name,
                "roll_number": (
                    profile.roll_number
                    if profile else ""
                ),
                "submitted_at": submission.submitted_at
            })

        return Response(data)

# =========================
# NOT SUBMITTED STUDENTS
# =========================

class NotSubmittedStudentsAPI(APIView):

    def get(self, request, pk):

        try:
            assignment = Assignment.objects.get(
                pk=pk
            )

        except Assignment.DoesNotExist:
            return Response(
                {"error": "Assignment not found"},
                status=404
            )

        submitted_ids = Submission.objects.filter(
            assignment=assignment
        ).values_list(
            "student_id",
            flat=True
        )

        students = StudentProfile.objects.select_related(
            "user"
        ).exclude(
            user_id__in=submitted_ids
        )

        data = []

        for student in students:

            data.append({
                "student_name": student.user.name,
                "roll_number": student.roll_number
            })

        return Response(data)


# =========================
# SUBMISSION DETAIL
# =========================

class SubmissionDetailAPI(APIView):

    def get(self, request, pk):

        try:
            submission = Submission.objects.select_related(
                "student",
                "assignment"
            ).get(pk=pk)

        except Submission.DoesNotExist:
            return Response(
                {"error": "Submission not found"},
                status=404
            )

        profile = StudentProfile.objects.filter(
            user=submission.student
        ).first()

        data = {
            "id": submission.id,
            "student_name": submission.student.name,
            "roll_number": (
                profile.roll_number
                if profile else ""
            ),
            "assignment_title":
                submission.assignment.title,
            "file":
                submission.file.url,
            "submitted_at":
                submission.submitted_at,
        }

        return Response(data)