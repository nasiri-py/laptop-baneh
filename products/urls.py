from django.urls import path, re_path
from . import views


app_name = 'product'
urlpatterns = [
    path('', views.product_list_view, name='list'),
    re_path(r'(?P<slug>[-\w]+)/\\Z', views.ProductDetailView.as_view(), name='detail'),
    path('<int:pk>/add-comment/', views.CommentView.as_view(), name='add-comment'),
    path('<int:product_pk>/<int:comment_pk>/add-reply/', views.CommentReplyView.as_view(), name='add-reply'),
    path('search/', views.search_view, name='search'),
    path('search-list/', views.SearchList.as_view(), name='search-list'),

]
