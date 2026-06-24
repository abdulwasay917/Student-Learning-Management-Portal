from django.urls import path, include
from . import views

urlpatterns = [
    path("api/", include("meetings.api.urls")),

    # HTML pages (future use)
    path("", views.meeting_page, name="meeting-page"),
    path("create/", views.create_meeting_page, name="meeting-create-page"),
    path("edit/<int:pk>/", views.update_meeting_page, name="meeting-edit"),
]