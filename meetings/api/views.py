from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from meetings.models import Meeting
from .serializers import MeetingSerializer


class MeetingListAPI(APIView):

    def get(self, request):

        meetings = Meeting.objects.filter(
            expires_at__gt=timezone.now()
        ).order_by("-created_at")

        serializer = MeetingSerializer(meetings, many=True)

        return Response(serializer.data)

class CreateMeetingAPI(APIView):

    def post(self, request):

        if not (
            request.user.role == "teacher"
            or request.user.is_superuser
        ):
            return Response(
                {"error": "Permission denied"},
                status=403
            )

        serializer = MeetingSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(
                teacher=request.user
            )

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class UpdateMeetingAPI(APIView):

    def put(self, request, pk):

        try:
            meeting = Meeting.objects.get(pk=pk)

        except Meeting.DoesNotExist:
            return Response(
                {"error": "Meeting not found"},
                status=404
            )

        # permission check
        if not (
            request.user.is_superuser
            or meeting.teacher == request.user
        ):
            return Response(
                {"error": "Not allowed"},
                status=403
            )

        serializer = MeetingSerializer(
            meeting,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class DeleteMeetingAPI(APIView):

    def delete(self, request, pk):

        try:
            meeting = Meeting.objects.get(pk=pk)

        except Meeting.DoesNotExist:
            return Response(
                {"error": "Meeting not found"},
                status=404
            )

        # permission check
        if not (
            request.user.is_superuser
            or meeting.teacher == request.user
        ):
            return Response(
                {"error": "Not allowed"},
                status=403
            )

        meeting.delete()

        return Response(
            {"message": "Meeting deleted"},
            status=200
        )