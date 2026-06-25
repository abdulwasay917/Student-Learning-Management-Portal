from django.db import models

from accounts.models import User


class Assignment(models.Model):

    title = models.CharField(max_length=255)

    statement = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Submission(models.Model):

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    file = models.FileField(
        upload_to="assignments/submissions/"
    )

    submitted_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = (
            "assignment",
            "student"
        )

    def __str__(self):
        return f"{self.student.name} - {self.assignment.title}"