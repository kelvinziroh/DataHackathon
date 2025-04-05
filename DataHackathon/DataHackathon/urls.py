from django.contrib import admin
from django.urls import path, include
from allauth.socialaccount.urls import urlpatterns as social_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include('hackathon.urls')),
]