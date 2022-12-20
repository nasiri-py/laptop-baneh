from django.urls import path
from .views import HomeView, contact_view

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', contact_view, name='contact'),
]
