from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, TeacherProfile


class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {
            "fields": ("name", "role", "phone")
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {
            "fields": ("name", "role", "phone")
        }),
    )

    list_display = ("username", "email", "name", "role", "is_staff", "is_active")
    search_fields = ("username", "email", "name")
    list_filter = ("role", "is_staff", "is_active")


admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)