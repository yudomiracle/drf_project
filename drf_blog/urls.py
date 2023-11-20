from django.urls import path

from drf_blog.views import post_list, post_detail, authenticate_user, register_user, login_user, logout_user

urlpatterns = [
    path('api/posts/', post_list, name='post_list'),
    path('api/posts/<int:pk>', post_detail, name='post_detail'),
    path('api/authenticate/', authenticate_user, name='authenticate_user'),
    path('api/register/', register_user, name='register_user'),
    path('api/login/', login_user, name='login_user'),
    path('api/logout/', logout_user, name='logout_user'),
]