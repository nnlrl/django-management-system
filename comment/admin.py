from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'author', 'post', 'timestamp', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('author',)
    fields = ("body", 'author', 'post', 'is_active')