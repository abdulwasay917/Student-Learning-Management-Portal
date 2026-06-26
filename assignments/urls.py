from django.urls import path, include

from assignments.views import (assignment_page,submitted_students_page,not_submitted_students_page,submission_detail_page,create_assignment_page)

urlpatterns = [
    path("",assignment_page,name="assignments-page"    ),
    path("submitted/<int:pk>/",submitted_students_page,name="submitted-page"),
    path("not-submitted/<int:pk>/",not_submitted_students_page,name="not-submitted-page"),
    path("submission/<int:pk>/",submission_detail_page,name="submission-detail-page"),
    path("api/",include("assignments.api.urls")),
    path("create/",create_assignment_page,name="create-assignment-page"),
]