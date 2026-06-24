from django.shortcuts import render


def meeting_page(request):
    return render(request, "meetings/list.html")


def create_meeting_page(request):
    return render(request, "meetings/create.html")

def update_meeting_page(request, pk):
    return render(request, "meetings/edit.html", {"pk": pk})