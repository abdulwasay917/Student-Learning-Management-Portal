from django.contrib import admin

from assignments.models import (
    Assignment,
    Submission
)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "created_by",
        "created_at",
    )

    search_fields = (
        "title",
        "created_by__username",
        "created_by__name",
    )

    list_filter = (
        "created_at",
    )


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "assignment",
        "student",
        "submitted_at",
    )

    search_fields = (
        "student__username",
        "student__name",
        "assignment__title",
    )

    list_filter = (
        "submitted_at",
    )