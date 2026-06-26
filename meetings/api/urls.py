from django.urls import path
from .views import (
    MeetingListAPI,
    CreateMeetingAPI,
    UpdateMeetingAPI,
    DeleteMeetingAPI
)

urlpatterns = [
    path("", MeetingListAPI.as_view()),
    path("create/", CreateMeetingAPI.as_view()),

    path("update/<int:pk>/", UpdateMeetingAPI.as_view()),
    path("delete/<int:pk>/", DeleteMeetingAPI.as_view()),
]