from django.urls import path

from .views import *

app_name = 'post'

urlpatterns = [
    path('', post, name='post'),
    path('<int:id>/<slug:slug>/', post_detail, name='post_detail'),
    path('search/', post_search, name='post_search'),
    path('category/<str:parent>/', post_category_search,
         name='post_category_search'),
    path('category/<str:parent>/<str:child>/', post_category_search,
         name='post_category_search'),
    path('tag/<slug:slug>/', post_tag_search, name='post_tag_search'),
]
