"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

# 存放映射关系的列表
urlpatterns = [
    # django自带后台
    path('admin/', admin.site.urls),
    # 配置app的根路由地址（url）
    # 主页
    path('home', views.my_home, name='my_home'),
    # 关于我
    path('about-me', views.about_me, name='about_me'),
    # 文章列表
    path('article/', include('article.urls', namespace='article')),
    # 文章管理后台
    path('my-admin/', include('myadmin.urls', namespace='myadmin')),    # 逗号！！！
    # 用户管理
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    # 第三方库：重置密码
    path('password-reset/', include('password_reset.urls')),
    # 第三方库：评论
    path('comment/', include('comment.urls', namespace='comment')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
