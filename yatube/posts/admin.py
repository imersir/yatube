from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Вывод в навигацию для GroupAdmin"""
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('description',)  # Строка поиска
    list_filter = ('title',)  # Боковая навигация
    empty_value_display = '-пусто-'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Вывод в навигацию для PostAdmin"""
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)  # Строка поиска
    list_filter = ('pub_date',)  # Боковая навигация
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Вывод в навигацию для CommentAdmin"""
    list_display = ('post', 'author', 'text', 'created',)
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Вывод в навигацию для FollowAdmin"""
    list_display = ('user', 'author')
    list_filter = ('user', 'author')
