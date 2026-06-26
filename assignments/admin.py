from django.contrib import admin

from assignments.models import (
    Assignment,
    Submission
)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    list_display = ("id","title","created_by","created_at",    )


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    list_display = ("id","assignment","student","submitted_at",)