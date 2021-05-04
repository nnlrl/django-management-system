"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
import notifications.urls

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('admin/', admin.site.urls),
    # 127.0.0.1:8000/index(主页相关路由)
    path('', include("index.urls")),
    # 127.0.0.1:8000/user(用户系统相关路由)
    path('user/', include("user.urls")),
    path('captcha/', include('captcha.urls')),  # 图片验证码 路由
    path('post/', include('post.urls')),
    path('order/', include('order.urls')),
    path('comment/', include('comment.urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found_404
handler500 = views.system_error_500
