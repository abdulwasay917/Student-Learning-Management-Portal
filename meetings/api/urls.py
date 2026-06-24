from django.urls import path
from .views import MeetingListAPI, CreateMeetingAPI

urlpatterns = [
    path("", MeetingListAPI.as_view(), name="meeting-list"),
    path("create/", CreateMeetingAPI.as_view(), name="meeting-create"),
]