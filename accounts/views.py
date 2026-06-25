from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        pass
    return render(request, "accounts/login.html")


@login_required(login_url="/accounts/login/")
def create_user_view(request):
    if request.method == "POST":
        pass
    return render(request, "accounts/create_user.html")


def forgot_password_view(request):
    if request.method == "POST":
        pass
    return render(request, "accounts/forgot.html")


def reset_password_view(request, uidb64, token):
    if request.method == "POST":
        pass
    return render(request, "accounts/reset_password.html")


@login_required(login_url="/accounts/login/")
def student_list_view(request):
    return render(request,"accounts/student_list.html")


@login_required(login_url="/accounts/login/")
def teacher_list_view(request):
    return render(request,"accounts/teacher_list.html")