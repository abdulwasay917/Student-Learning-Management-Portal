from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("",lambda request: redirect('dashboard')),
    path('admin/', admin.site.urls),
    path("accounts/", include('accounts.urls')),
    path("core/", include("core.urls")),
    path("meetings/", include("meetings.urls")),
    path("assignments/", include("assignments.urls")),
    path( 'token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
