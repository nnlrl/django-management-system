import bleach
from django.conf import settings
from django.db import models
from markdown import markdown


# Create your models here.
class Post(models.Model):
    title = models.CharField(verbose_name="标题", max_length=150)
    introduction = models.CharField(verbose_name="简介", max_length=150)
    body = models.TextField(verbose_name="内容")
    timestamp = models.DateTimeField(verbose_name="创建日期", db_index=True, auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body_html = models.TextField(verbose_name="内容(html)", default='')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="post_like", blank=True)
    is_active = models.BooleanField(verbose_name="是否激活", default=True)
    is_open = models.BooleanField(verbose_name="是否公开", default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "博客管理"
        verbose_name_plural = verbose_name

    @staticmethod
    def to_html(value):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote',
                      'code', 'em', 'i', 'li', 'ol', 'pre',
                      'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html5',
                                                         extensions=['markdown.extensions.toc',
                                                                     'markdown.extensions.fenced_code',
                                                                     'markdown.extensions.tables']),
                                                tags=allow_tags, strip=True))
        return body_html
