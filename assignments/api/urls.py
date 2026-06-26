from django.urls import path

from assignments.api.views import (AssignmentListAPI,CreateAssignmentAPI,DeleteAssignmentAPI,SubmitAssignmentAPI,SubmittedStudentsAPI,NotSubmittedStudentsAPI,SubmissionDetailAPI,)

urlpatterns = [
    path("",AssignmentListAPI.as_view(),name="assignment-list"),
    path("create/",CreateAssignmentAPI.as_view(),name="assignment-create"),
    path("delete/<int:pk>/",DeleteAssignmentAPI.as_view(),name="assignment-delete"),
    path("submit/<int:pk>/",SubmitAssignmentAPI.as_view(),name="assignment-submit"),
    path("submitted/<int:pk>/",SubmittedStudentsAPI.as_view(),name="submitted-students"),
    path("not-submitted/<int:pk>/",NotSubmittedStudentsAPI.as_view(),name="not-submitted-students"),
    path("submission/<int:pk>/",SubmissionDetailAPI.as_view(),name="submission-detail"),
]