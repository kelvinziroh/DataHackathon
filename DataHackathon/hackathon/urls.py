from django.urls import path
from . import views

app_name = 'hackathon'
urlpatterns = [
    path('status/', views.auth_status, name='auth_status'),
]