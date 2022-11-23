from django.urls import path, re_path
from . import views


app_name = 'product'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    re_path(r'(?P<slug>[-\w]+)/\\Z', views.ProductDetailView.as_view(), name='detail'),
]
