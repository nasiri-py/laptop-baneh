from django.urls import path, re_path
from . import views


app_name = 'product'
urlpatterns = [
    path('', views.product_list_view, name='list'),
    re_path(r'detail/(?P<slug>[-\w]+)/', views.ProductDetailView.as_view(), name='detail'),
    path('<int:pk>/add-comment/', views.CommentView.as_view(), name='add-comment'),
    path('<int:product_pk>/<int:comment_pk>/add-reply/', views.CommentReplyView.as_view(), name='add-reply'),
    path('search/', views.search_view, name='search'),
    path('search-list/', views.SearchList.as_view(), name='search-list'),
    path('compare/', views.compare_view, name='compare'),
    path('compare/add/<int:pk>/', views.compare_add_view, name='compare-add'),
    path('compare/delete/<int:pk>/', views.compare_delete_view, name='compare-delete'),
    path('compare/search/', views.compare_search_view, name='compare-search'),
]
