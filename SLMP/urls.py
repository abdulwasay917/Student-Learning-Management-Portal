from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path("",lambda request: redirect('dashboard')),
    path('admin/', admin.site.urls),
    path("accounts/", include('accounts.urls')),
    path("core/", include("core.urls")),
    path("meetings/", include("meetings.urls")),
    path("assignments/", include("assignments.urls")),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
