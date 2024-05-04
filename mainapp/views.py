from django.views.generic import ListView, DetailView
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'
    paginate_by = 5


class AboutView(ListView):
    model = Article
    template_name = 'mainapp/about.html'
    context_object_name = 'articles'
    paginate_by = 5


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'mainapp/article.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'
