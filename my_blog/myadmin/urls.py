from django.urls import path
from . import views     # !!!

app_name = 'myadmin'

urlpatterns = [
    path('home/' , views.home , name='admin_home'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    path('create/', views.create , name='admin_create'),
    path('delete/', views.delete , name='admin_delete'),
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    path('article-safe-delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),
    path('update/', views.update , name='admin_update'),
    path('article-update/<int:id>/', views.article_update, name='article_update'),
    path('chart/', views.chart, name='chart'),
    path('comment/', views.comment, name='comment'),    
    path('comment-delete/<int:id>/', views.comment_delete, name='comment_delete'),
]
