from django.shortcuts import render


def meeting_page(request):
    return render(request, "meetings/list.html")


def create_meeting_page(request):
    return render(request, "meetings/create.html")