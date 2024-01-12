from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.models import Blog, Tag, Category, Comment, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
