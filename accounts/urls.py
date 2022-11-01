from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
