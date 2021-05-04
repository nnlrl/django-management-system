from django.contrib import admin
from .models import Post
from comment.models import Comment


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'introduction', 'timestamp', 'author', '_userid', '_likes',
                    'is_active', 'is_open')
    list_filter = ('timestamp', 'is_active', 'is_open')
    search_fields = ('title',)
    fields = ('title', 'introduction', 'body', 'author', 'is_active', 'is_open')

    def _userid(self, obj):
        return obj.author.userid

    def _likes(self, obj):
        return len(obj.likes.all())



