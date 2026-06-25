from django.shortcuts import render


def assignment_page(request):
    return render(
        request,
        "assignments/list.html"
    )


def submitted_students_page(
    request,
    pk
):
    return render(
        request,
        "assignments/submitted_students.html",
        {"pk": pk}
    )


def not_submitted_students_page(
    request,
    pk
):
    return render(
        request,
        "assignments/not_submitted_students.html",
        {"pk": pk}
    )


def submission_detail_page(
    request,
    pk
):
    return render(
        request,
        "assignments/submission_detail.html",
        {"pk": pk}
    )

def create_assignment_page(request):
    return render(
        request,
        "assignments/create.html"
    )