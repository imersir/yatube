from django.contrib import admin

from .models import Group, Post


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
