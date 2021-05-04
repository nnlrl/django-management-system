import bleach
from django.conf import settings
from django.db import models
from markdown import markdown

from post.models import Post


# Create your models here.
class Comment(models.Model):
    body = models.TextField(verbose_name="内容")
    body_html = models.TextField(verbose_name="内容(html)", default='')
    timestamp = models.DateTimeField(verbose_name="评论日期", db_index=True, auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="是否激活", default=True)

    class Meta:
        verbose_name = "评论管理"
        verbose_name_plural = verbose_name

    @staticmethod
    def to_html(value):
        allow_tags = ['a', 'abbr', 'acronym', 'b',
                      'code', 'em', 'i', 'strong']
        body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html5',
                                                         extensions=['markdown.extensions.toc',
                                                                     'markdown.extensions.fenced_code',
                                                                     'markdown.extensions.tables']),
                                                tags=allow_tags, strip=True))
        return body_html
