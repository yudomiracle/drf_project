from django.contrib import admin

# Register your models here.
from drf_blog.models import Author, Post, Like, Comment

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)