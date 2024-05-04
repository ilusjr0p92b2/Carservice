from django.contrib import admin
from django.urls import path, include

from mainapp.views import ArticleListView, ArticleDetailView, AboutView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('article/<int:article_id>', ArticleDetailView.as_view(), name='article'),
]
