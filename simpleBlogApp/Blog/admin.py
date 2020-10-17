from django.contrib import admin
from .models import UserBlog, BlogPost


@admin.register(UserBlog, BlogPost)
class BlogAdmin(admin.ModelAdmin):
    pass