from rest_framework import serializers

from assignments.models import (
    Assignment,
    Submission
)


class AssignmentSerializer(serializers.ModelSerializer):

    teacher_name = serializers.CharField(
        source="created_by.name",
        read_only=True
    )

    creator_id = serializers.IntegerField(
        source="created_by.id",
        read_only=True
    )

    submitted_count = serializers.SerializerMethodField()

    class Meta:
        model = Assignment

        fields = [
            "id",
            "title",
            "statement",
            "teacher_name",
            "creator_id",
            "submitted_count",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "teacher_name",
            "submitted_count",
            "created_at",
        ]

    def get_submitted_count(self, obj):
        return obj.submissions.count()


class SubmissionSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source="student.name",
        read_only=True
    )

    class Meta:
        model = Submission

        fields = [
            "id",
            "student_name",
            "file",
            "submitted_at",
        ]

        read_only_fields = [
            "id",
            "student_name",
            "submitted_at",
        ]