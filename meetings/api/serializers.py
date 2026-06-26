from rest_framework import serializers
from meetings.models import Meeting


class MeetingSerializer(serializers.ModelSerializer):

    teacher_name = serializers.CharField(source="teacher.name",read_only=True)

    class Meta:
        model = Meeting
        fields = [
            "id",
            "title",
            "link",
            "teacher_name",
            "created_at",
            "expires_at",
        ]
        read_only_fields = [
            "id",
            "teacher_name",
            "created_at",
            "expires_at",
        ]