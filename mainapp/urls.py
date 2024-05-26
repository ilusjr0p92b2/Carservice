from django.urls import path

from mainapp.views import ArticleListView, ArticleDetailView, AboutView, CommentDeleteView, EditArticleView, DeleteArticleView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article'),
    path('edit_article/<int:pk>', EditArticleView.as_view(), name='edit_article'),
    path('delete_article/<int:pk>', DeleteArticleView.as_view(), name='delete_article'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
]
