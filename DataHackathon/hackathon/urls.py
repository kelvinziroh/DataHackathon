from django.urls import path
from .views import RegisterView, LoginView
from . import views

app_name = 'hackathon'
urlpatterns = [
    path('status/', views.auth_status, name='auth_status'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
]