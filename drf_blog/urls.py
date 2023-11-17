from django.urls import path

from drf_blog.views import post_list, post_detail

urlpatterns = [
    path('api/posts', post_list, name='post_list'),
    path('api/posts/<int:pk>', post_detail, name='post_detail')
]